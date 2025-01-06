#include <string>
#include "aoc_common.h"

namespace aoc_common {

std::string getFilenameFromCliArgs(int argc, char **argv) {
    return argv[argc - 1];
}

} // namespace aoc {
