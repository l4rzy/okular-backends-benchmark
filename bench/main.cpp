// SPDX-License-Identifier: GPL-3.0-or-later
#include "workload.hpp"

#include <KConfigGroup>
#include <KPluginMetaData>
#include <KSharedConfig>
#include <QApplication>
#include <QCommandLineParser>
#include <QDateTime>
#include <QDir>
#include <QElapsedTimer>
#include <QEventLoop>
#include <QFile>
#include <QFileInfo>
#include <QJsonArray>
#include <QJsonDocument>
#include <QJsonObject>
#include <QMimeDatabase>
#include <QTemporaryDir>
#include <QTextStream>
#include <QTimer>
#include <QUrl>

#include <okular/core/document.h>
#include <okular/core/generator.h>
#include <okular/core/observer.h>
#include <okular/core/page.h>
#include <okular/core/settings_core.h>

#include <cmath>
#include <functional>

namespace {

class Observer final : public Okular::DocumentObserver {
public:
    std::function<void()> onPixmap;

    void notifyPageChanged(int, int flags) override
    {
        if ((flags & Pixmap) && onPixmap)
            onPixmap();
    }
};

int finish(QJsonObject report, const QString& error = { })
{
    report["status"] = error.isEmpty() ? "ok" : "error";
    if (!error.isEmpty())
        report["error"] = error;
    QTextStream(stdout) << QJsonDocument(report).toJson(QJsonDocument::Compact) << '\n';
    return error.isEmpty() ? 0 : 1;
}

} // namespace

int main(int argc, char** argv)
{
    // Establish isolated state before Qt/KConfig can read desktop preferences.
    QTemporaryDir root;
    if (!root.isValid())
        return finish({ }, "Cannot create temporary benchmark directory");
    for (const auto& kind : { "CONFIG", "CACHE", "DATA" })
        qputenv(QByteArray("XDG_") + kind + "_HOME", root.filePath(kind).toUtf8());
    QApplication app(argc, argv);
    QCoreApplication::setApplicationName("okular-bench");
    QCommandLineParser parser;
    parser.setApplicationDescription("Measure Okular backend page delivery; emits one JSON report.");
    parser.addHelpOption();
    parser.addOptions({ { "backend", "Backend: mupdfng or poppler", "name" },
                        { "library", "Absolute generator library path (otherwise discover by backend)", "path" },
                        { "pdf", "PDF to open", "path" },
                        { "width", "Page width in pixels; height preserves aspect ratio", "pixels", "1200" },
                        { "pages", "Maximum pages per workload phase", "count", "10" },
                        { "expected-pages", "Required document page count from the corpus manifest", "count" },
                        { "seed", "Random jump seed", "number", "1" },
                        { "timeout-ms", "Timeout for each page request", "milliseconds", "30000" } });
    parser.process(app);
    const QString backend = parser.value("backend");
    QJsonObject report { { "backend", backend }, { "qt_version", qVersion() }, { "build_type", BENCH_BUILD_TYPE } };
    if (backend != "mupdfng" && backend != "poppler")
        return finish(report, "--backend must be mupdfng or poppler");
    bool widthOk = false, pagesOk = false, timeoutOk = false, seedOk = false;
    const int width = parser.value("width").toInt(&widthOk);
    const int count = parser.value("pages").toInt(&pagesOk);
    const int timeoutMs = parser.value("timeout-ms").toInt(&timeoutOk);
    const unsigned int seed = parser.value("seed").toUInt(&seedOk);
    if (!widthOk || width < 1 || width > 16384 || !pagesOk || count < 1 || !timeoutOk || timeoutMs < 1 || !seedOk)
        return finish(report, "Invalid width (1..16384), pages (>0), timeout (>0), or seed (uint32)");
    bool expectedPagesOk = false;
    const int expectedPages = parser.value("expected-pages").toInt(&expectedPagesOk);
    if (parser.isSet("expected-pages") && (!expectedPagesOk || expectedPages < 1))
        return finish(report, "--expected-pages must be a positive integer");
    const QString pdf = QFileInfo(parser.value("pdf")).canonicalFilePath();
    if (pdf.isEmpty() || !QFileInfo(pdf).isFile() || QFileInfo(pdf).suffix().compare("pdf", Qt::CaseInsensitive) != 0)
        return finish(report, "--pdf must name an existing PDF file");

    const QString expectedId = "okularGenerator_" + backend;
    const auto metadata = parser.isSet("library")
        ? KPluginMetaData(QFileInfo(parser.value("library")).absoluteFilePath())
        : KPluginMetaData::findPluginById("okular_generators", expectedId);
    if (!metadata.isValid() || metadata.pluginId() != expectedId) {
        report["discovered_plugin_id"] = metadata.pluginId();
        report["discovered_plugin_path"] = metadata.fileName();
        return finish(report, "Cannot find requested generator: " + expectedId);
    }
    const QString plugin = QFileInfo(metadata.fileName()).canonicalFilePath();
    const QString staging = root.filePath("plugins");
    if (!QDir().mkpath(staging + "/okular_generators")
        || !QFile::link(plugin, staging + "/okular_generators/" + QFileInfo(metadata.fileName()).fileName()))
        return finish(report, "Cannot stage generator library");
    // Only this generator is discoverable; fail rather than silently use another.
    QCoreApplication::setLibraryPaths({ staging });
    const auto available = KPluginMetaData::findPlugins("okular_generators");
    if (available.size() != 1 || available.front().pluginId() != expectedId)
        return finish(report, "Generator isolation failed");

    Okular::SettingsCore::instance("okular-bench");
    const auto config = KSharedConfig::openConfig("okular-mupdf-ngrc");
    KConfigGroup(config, "OCR").writeEntry("OcrTriggerMode", "Never");
    KConfigGroup(config, "General").writeEntry("HeuristicSynopsisEnabled", false);
    // Match the generator tests: use every available worker protection without
    // replacing the document with a Strict-mode gate page on container runners.
    KConfigGroup(config, "General").writeEntry("SandboxEnforcement", "Relaxed");
    KConfigGroup(config, "Advanced")
        .writeEntry("CacheLastVacuum", QDateTime::currentDateTimeUtc().toString(Qt::ISODate));
    config->sync();
    report["plugin_path"] = plugin;
    report["plugin_version"] = metadata.version();
    report["pdf"] = pdf;
    report["width"] = width;
    report["seed"] = static_cast<qint64>(seed);
    report["profile"] = "common-pdf-features";
    report["sandbox_enforcement"] = "Relaxed";
    report["filesystem_cache"] = "uncontrolled";

    Observer observer;
    Okular::Document document(nullptr);
    QString documentError;
    QJsonArray warnings;
    QObject::connect(
        &document, &Okular::Document::error, &app, [&](const QString& message, int) { documentError = message; });
    QObject::connect(
        &document, &Okular::Document::warning, &app, [&](const QString& message, int) { warnings.append(message); });
    document.addObserver(&observer);
    QElapsedTimer opening;
    opening.start();
    const auto opened =
        document.openDocument(pdf, QUrl::fromLocalFile(pdf), QMimeDatabase().mimeTypeForName("application/pdf"));
    report["open_ms"] = static_cast<double>(opening.nsecsElapsed()) / 1e6;
    if (opened != Okular::Document::OpenSuccess) {
        report["warnings"] = warnings;
        return finish(report, documentError.isEmpty() ? "Document open failed (passwords unsupported)" : documentError);
    }
    if (QFileInfo(document.generatorInfo().fileName()).canonicalFilePath() != plugin)
        return finish(report, "Loaded generator does not match requested library");
    report["page_count"] = static_cast<int>(document.pages());
    if (parser.isSet("expected-pages") && document.pages() != static_cast<uint>(expectedPages)) {
        document.removeObserver(&observer);
        document.closeDocument();
        return finish(report,
                      QString("%1: %2 reported %3 pages; corpus expects %4. Refusing to benchmark a placeholder or "
                              "incomplete document.")
                          .arg(pdf, backend)
                          .arg(report["page_count"].toInt())
                          .arg(expectedPages));
    }
    QJsonArray samples;
    QString failure;
    for (const auto& request : Bench::makeRequests(static_cast<int>(document.pages()), count, seed)) {
        const auto* page = document.page(request.page);
        const double scaledHeight = static_cast<double>(width) * page->height() / page->width();
        if (!std::isfinite(scaledHeight) || scaledHeight < 1 || scaledHeight > 32768) {
            failure = "Page aspect ratio produces unsupported render dimensions";
            break;
        }
        const int height = static_cast<int>(std::lround(scaledHeight));
        const auto ready = [&] {
            return page->hasPixmap(&observer, width, height);
        };
        const bool cached = ready();
        QEventLoop loop;
        QTimer timer;
        timer.setSingleShot(true);
        QObject::connect(&timer, &QTimer::timeout, &loop, &QEventLoop::quit);
        observer.onPixmap = [&] {
            if (ready())
                loop.quit();
        };
        QElapsedTimer elapsed;
        elapsed.start();
        auto* pixmapRequest = new Okular::PixmapRequest(
            &observer, request.page, width, height, 1, 0, Okular::PixmapRequest::Asynchronous);
        pixmapRequest->setPartialUpdatesWanted(false);
        document.requestPixmaps({ pixmapRequest });
        if (!ready()) {
            timer.start(timeoutMs);
            loop.exec();
        }
        const double milliseconds = static_cast<double>(elapsed.nsecsElapsed()) / 1e6;
        observer.onPixmap = { };
        const bool success = ready() && documentError.isEmpty();
        samples.append(QJsonObject {
            { "phase", QString::fromLatin1(request.phase.data(), static_cast<qsizetype>(request.phase.size())) },
            { "page", request.page },
            { "width", width },
            { "height", height },
            { "cached_before", cached },
            { "elapsed_ms", milliseconds },
            { "ok", success } });
        if (request.phase == "first_page" && success)
            report["open_to_first_page_ms"] = static_cast<double>(opening.nsecsElapsed()) / 1e6;
        if (!success) {
            failure = documentError.isEmpty() ? "Page request timed out" : documentError;
            break;
        }
    }
    report["samples"] = samples;
    report["warnings"] = warnings;
    if (document.pages() == 0)
        failure = "Document contains no pages";
    document.removeObserver(&observer);
    document.closeDocument();
    return finish(report, failure);
}
