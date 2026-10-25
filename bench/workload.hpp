// SPDX-License-Identifier: GPL-3.0-or-later
#pragma once

#include <algorithm>
#include <random>
#include <string_view>
#include <vector>

namespace Bench {

struct Request {
    std::string_view phase;
    int page;
    bool operator==(const Request&) const = default;
};

// Keep the page sequence independent of backend timing and cache behaviour.
inline std::vector<Request> makeRequests(int pageCount, int sampleCount, unsigned int seed)
{
    if (pageCount <= 0 || sampleCount <= 0)
        return { };
    const int count = std::min(pageCount, sampleCount);
    std::vector<Request> requests { { "first_page", 0 } };
    for (int page = 1; page < count; ++page)
        requests.push_back({ "sequential", page });
    std::mt19937 random(seed);
    std::uniform_int_distribution<int> page(0, pageCount - 1);
    std::vector<int> jumps;
    for (int index = 0; index < count; ++index) {
        jumps.push_back(page(random));
        requests.push_back({ "random", jumps.back() });
    }
    for (auto it = jumps.rbegin(); it != jumps.rend(); ++it)
        requests.push_back({ "revisit", *it });
    return requests;
}

} // namespace Bench
