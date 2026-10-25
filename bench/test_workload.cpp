// SPDX-License-Identifier: GPL-3.0-or-later
#include "workload.hpp"

#include <QTest>

class TestWorkload : public QObject {
    Q_OBJECT
private slots:

    void requests_data()
    {
        QTest::addColumn<int>("pages");
        QTest::addColumn<int>("limit");
        QTest::addColumn<int>("count");
        QTest::newRow("empty") << 0 << 10 << 0;
        QTest::newRow("negative") << -1 << 10 << 0;
        QTest::newRow("zero-limit") << 10 << 0 << 0;
        QTest::newRow("single-page") << 1 << 10 << 3;
        QTest::newRow("cap-at-document") << 3 << 10 << 9;
        QTest::newRow("sample-long-document") << 100 << 5 << 15;
    }

    void requests()
    {
        QFETCH(int, pages);
        QFETCH(int, limit);
        QFETCH(int, count);
        const auto requests = Bench::makeRequests(pages, limit, 42);
        QCOMPARE(static_cast<int>(requests.size()), count);
        QVERIFY(requests == Bench::makeRequests(pages, limit, 42));
        if (requests.empty())
            return;
        QCOMPARE(requests.front().page, 0);
        QVERIFY(requests.front().phase == "first_page");
        const int samples = count / 3;
        for (int index = 0; index < count; ++index) {
            const auto& request = requests[static_cast<std::size_t>(index)];
            QVERIFY(request.page >= 0 && request.page < pages);
            if (index < samples) {
                QCOMPARE(request.page, index);
                if (index > 0)
                    QVERIFY(request.phase == "sequential");
            } else if (index < 2 * samples) {
                QVERIFY(request.phase == "random");
            } else {
                QVERIFY(request.phase == "revisit");
                QCOMPARE(request.page, requests[static_cast<std::size_t>(4 * samples - 1 - index)].page);
            }
        }
    }
};

QTEST_GUILESS_MAIN(TestWorkload)
#include "test_workload.moc"
