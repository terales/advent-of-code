Build from current folder using LLVM 19:

```bash
cmake -Wno-dev -D CMAKE_C_COMPILER=/opt/homebrew/opt/llvm/bin/clang -D CMAKE_CXX_COMPILER=/opt/homebrew/opt/llvm/bin/clang++  ./
cmake --build .
```

For Zed editor configure:
```bash
"lsp": {
  "clangd": {
    "binary": {
      "path": "/opt/homebrew/opt/llvm/bin/clangd",
      "arguments": ["-log=verbose", "--background-index", "-pretty", "--clang-tidy"]
    }
  }
},
"languages": {
  "C++": {
    "format_on_save": "on",
    "formatter": {
      "external": {
        "command": "/opt/homebrew/opt/llvm/bin/clang-format",
        "arguments": ["--style=file", "--assume-filename={buffer_path}"]
      }
    }
  }
}
```
