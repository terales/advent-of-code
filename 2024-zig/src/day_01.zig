const std = @import("std");
const aoc_utils = @import("aoc_utils_lib");

pub fn main() !void {
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();
    defer {
        const deinit_status = gpa.deinit();
        if (deinit_status == .leak) @panic("Memory leak detected!");
    }

    const content = try aoc_utils.getInputContent(allocator);
    defer allocator.free(content);

    var splitSequence = std.mem.tokenizeAny(u8, content, " \n");

    while (splitSequence.next()) |token| {
        std.debug.print("{s}\n", .{token});
    }
}
