#include <iostream>
#include <llvm/ADT/StringRef.h>

int main() {
    llvm::StringRef s = llvm::StringRef("a string");

    std::cout << std::string(s) << std::endl;
    return 0;
}
