const std = @import("std");
const aoc_utils = @import("aoc_utils_lib");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    const allocator = arena.allocator();
    defer arena.deinit();

    const content = try aoc_utils.getInputContent(allocator);
    var sumUnconditional: u32 = 0;
    var sumConditional: u32 = 0;
    var enabled = true;

    var dont_tokens = std.mem.tokenizeSequence(u8, content, "don't()");
    while (dont_tokens.next()) |dont_token| {
        var do_tokens = std.mem.tokenizeSequence(u8, dont_token, "do()");
        while (do_tokens.next()) |do_token| {
            const sumProducts = try runMultiplies(do_token);
            sumUnconditional = sumUnconditional + sumProducts;
            if (enabled) {
                sumConditional = sumConditional + sumProducts;
            }

            enabled = true;
        }
        enabled = false;
    }
    std.debug.print("Part 1: {d}\n", .{sumUnconditional});
    std.debug.print("Part 2: {d}\n", .{sumConditional});
}

fn runMultiplies(instructions: []const u8) !u32 {
    var sum: u32 = 0;
    var functions = std.mem.tokenizeSequence(u8, instructions, "mul(");
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
    return sum;
}
