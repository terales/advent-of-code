#include <algorithm>
#include <fstream>
#include <iostream>
#include <map>
#include <string>
#include <vector>
#include "aoc_common.h"

int main(int argc, char **argv) {
    std::string inputFilename = aoc_common::getFilenameFromCliArgs(argc, argv);
    std::ifstream inputStream(inputFilename, std::ios_base::in);

    int temp;
    std::vector<int> leftLocations;
    std::vector<int> rightLocations;
    bool isLeft = true;

    while (inputStream >> temp) {
        if (isLeft) {
            leftLocations.push_back(temp);
        } else {
            rightLocations.push_back(temp);
        }
        isLeft = !isLeft;
    }

    std::ranges::sort(leftLocations, std::ranges::less());
    std::ranges::sort(rightLocations, std::ranges::less());

    std::map<int, std::size_t> rightLocationOccurrences;
    for (const int location : rightLocations) {
        rightLocationOccurrences[location] += 1;
    }

    int totalDistance = 0;
    int similarityScore = 0;
    for (size_t i = 0; i < leftLocations.size(); i++) {
        totalDistance += std::abs(leftLocations[i] - rightLocations[i]);
        similarityScore += leftLocations[i] * rightLocationOccurrences[leftLocations[i]];
    }
    std::cout << "Total distance: " << totalDistance << "\n";
    std::cout << "Similarity score: " << similarityScore << "\n";

    return 0;
}
