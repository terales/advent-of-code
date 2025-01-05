#include <assert.h>
#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
#include <boost/algorithm/string_regex.hpp>
#include "aoc_common.h"

int main(int argc, char **argv) {
    const std::string inputFilename = aoc_common::getFilenameFromCliArgs(argc, argv);
    const std::string input = aoc_common::getStrippedInputStr(inputFilename);

    std::vector<std::string> locations;
    std::vector<int> leftLocations;
    std::vector<int> rightLocations;
    boost::algorithm::split_regex( locations, input, boost::regex( "(?:   |\n)" ));
    assert(locations.size() % 2 == 0);

    bool isLeft = true;
    for (size_t i = 0; i < locations.size(); i++) {
        if (isLeft) {
            leftLocations.push_back(std::stoi(locations[i]));
        } else {
            rightLocations.push_back(std::stoi(locations[i]));
        }
        isLeft = !isLeft;
    }

    std::ranges::sort(leftLocations, std::ranges::less());
    std::ranges::sort(rightLocations, std::ranges::less());

    std::vector<int> distances(leftLocations.size());
    for (size_t i = 0; i < leftLocations.size(); i++) {
        distances[i] = std::abs(rightLocations[i] - leftLocations[i]);
    }

    int totalDistance = std::ranges::fold_left(distances, 0, std::plus<int>());
    std::cout << "Total distance: " << totalDistance << "\n";

    return 0;
}
