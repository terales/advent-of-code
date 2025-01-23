const std = @import("std");
const aoc_utils = @import("aoc_utils_lib");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    const allocator = arena.allocator();
    defer arena.deinit();

    const content = try aoc_utils.getInputContent(allocator);
    var sum: u32 = 0;

    var functions = std.mem.tokenizeSequence(u8, content, "mul(");
    while (functions.next()) |function| {
        var paramsIterator = std.mem.tokenizeScalar(u8, function, ')');
        const params = paramsIterator.next();
        if (params == null) {
            continue;
        }

        var factors = std.mem.tokenizeScalar(u8, params orelse "", ',');
        const multiplier = std.fmt.parseUnsigned(u32, factors.next() orelse "", 10) catch |err| switch (err) {
            error.InvalidCharacter => continue,
            else => return err,
        };
        const multiplicand = std.fmt.parseUnsigned(u32, factors.next() orelse "", 10) catch |err| switch (err) {
            error.InvalidCharacter => continue,
            else => return err,
        };
        if (factors.next() != null) {
            continue; // continue for cases like "mul(12,34,sdfsfs)"
        }

        sum = sum + multiplier * multiplicand;
    }
    std.debug.print("Part 1: {d}\n", .{sum});
}
