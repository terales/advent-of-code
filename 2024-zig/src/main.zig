const std = @import("std");
pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("All your {s} are belong to us.\n", .{"challenges"});
    try stdout.print("Run `zig build test` to run the tests.\n", .{});
}
