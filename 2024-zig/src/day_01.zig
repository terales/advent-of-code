const std = @import("std");
const aoc_utils = @import("aoc_utils_lib");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    defer {
        const deinit_status = gpa.deinit();
        if (deinit_status == .leak) @panic("Memory leak detected!");
    }

    const inputFilePath: []const u8 = try aoc_utils.getInputFilePath(allocator);
    std.debug.print("File path: {?s}\n", .{inputFilePath});
}
