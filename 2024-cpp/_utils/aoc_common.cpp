#include <fstream>
#include <sstream>
#include <string>
#include <llvm/Support/CommandLine.h>
#include "aoc_common.h"

namespace aoc_common {

std::string getFilenameFromCliArgs(int argc, char **argv) {
    llvm::cl::opt<std::string> InputFilename(llvm::cl::Positional, llvm::cl::Required, llvm::cl::desc("<input file path>"));

    llvm::StringMap<llvm::cl::Option*> &Map = llvm::cl::getRegisteredOptions();

    assert(Map.count("color") > 0);
    Map["color"]->setHiddenFlag(llvm::cl::ReallyHidden);
    
    assert(Map.count("help") > 0);
    Map["help"]->setDescription("Shows help with list of available options");

    llvm::cl::ParseCommandLineOptions(argc, argv);
    return InputFilename;
}

std::string getStrippedInputStr(std::string filename) {
    // Read entire file into memory: // https://web.archive.org/web/20180314195042/cpp.indi.frih.net/blog/2014/09/how-to-read-an-entire-file-into-memory-in-cpp/
    std::ifstream inputStream(filename);
    std::basic_ostringstream<char> stringStream = std::ostringstream{};
    stringStream << inputStream.rdbuf();
    std::string input = stringStream.str();

    // Strip whitespaces
    std::size_t found = input.find_last_not_of(" \t\f\v\n\r");
    if (found!=std::string::npos)
        input.erase(found+1);
    else
        input.clear();

    return input;
}

} // namespace aoc {
