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

    int totalDistance = 0;
    int similarityScore = 0;
    for (size_t i = 0; i < leftLocations.size(); i++) {
        totalDistance += std::abs(leftLocations[i] - rightLocations[i]);
        similarityScore += leftLocations[i] * std::ranges::count(rightLocations, leftLocations[i]);
    }
    std::cout << "Total distance: " << totalDistance << "\n";
    std::cout << "Similarity score: " << similarityScore << "\n";

    return 0;
}
