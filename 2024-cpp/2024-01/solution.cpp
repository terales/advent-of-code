#include <iostream>
#include "aoc_common.h"

int main(int argc, char **argv) {
    const std::string inputFilename = aoc_common::getFilenameFromCliArgs(argc, argv);
    std::cout << inputFilename << std::endl;
    return 0;
}
