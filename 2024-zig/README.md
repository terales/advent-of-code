### Usage:

```bash
zig build
./zig-out/bin/day_01 ./data/01-input.txt
```

### Creating a new day

```zig
const std = @import("std");
const aoc_utils = @import("aoc_utils_lib");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    const allocator = arena.allocator();
    defer arena.deinit();

    const content = try aoc_utils.getInputContent(allocator);

    std.debug.print("Sample answer: {d}\n", .{content});
}
```
