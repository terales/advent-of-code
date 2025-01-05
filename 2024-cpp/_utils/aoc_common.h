#pragma once
#include <string>

namespace aoc_common {

std::string getFilenameFromCliArgs(int argc, char **argv);
std::string getStrippedInputStr(std::string filename);

}  // namespace aoc {
