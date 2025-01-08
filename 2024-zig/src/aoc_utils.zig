const std = @import("std");
const testing = std.testing;

pub fn getInputFilePath(allocator: std.mem.Allocator) ![]const u8 {
    var args = try std.process.argsWithAllocator(allocator);
    defer args.deinit();

    _ = args.skip(); // skip executable

    if (args.next()) |lastArg| {
        return lastArg;
    } else {
        return error.NoArgsReceived;
    }
}
