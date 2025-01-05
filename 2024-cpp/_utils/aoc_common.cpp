#include "aoc_common.h"
#include "llvm/Support/CommandLine.h"

namespace aoc_common {

std::string getFilenameFromCliArgs(int argc, char **argv) {
    llvm::cl::opt<std::string> InputFilename(llvm::cl::Positional, llvm::cl::Required, llvm::cl::desc("<input file>"));

    llvm::StringMap<llvm::cl::Option*> &Map = llvm::cl::getRegisteredOptions();

    assert(Map.count("color") > 0);
    Map["color"]->setHiddenFlag(llvm::cl::ReallyHidden);
    
    assert(Map.count("help") > 0);
    Map["help"]->setDescription("Shows help with list of available options");

    llvm::cl::ParseCommandLineOptions(argc, argv);
    return InputFilename;
}

} // namespace aoc {
