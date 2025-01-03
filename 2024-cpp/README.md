Build from current folder using LLVM 19:

```bash
cmake -Wno-dev .
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
