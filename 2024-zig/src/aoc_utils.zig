const std = @import("std");
const testing = std.testing;

pub fn getInputContent(allocator: std.mem.Allocator) ![]u8 {
    const file = try std.fs.cwd().openFile(
        try getInputFilePath(allocator),
        .{ .mode = .read_only },
    );
    defer file.close();

    return try file.readToEndAlloc(allocator, std.math.maxInt(usize));
}

fn getInputFilePath(allocator: std.mem.Allocator) ![]const u8 {
    var args = try std.process.argsWithAllocator(allocator);
    defer args.deinit();

    _ = args.skip(); // skip executable

    if (args.next()) |lastArg| {
        return lastArg;
    } else {
        return error.NoArgsReceived;
    }
}
