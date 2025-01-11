const std = @import("std");
const aoc_utils = @import("aoc_utils_lib");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    const allocator = arena.allocator();
    defer arena.deinit();

    var safeReports: u16 = 0;

    const content = try aoc_utils.getInputContent(allocator);
    var rawReports = std.mem.tokenizeScalar(u8, content, '\n');

    while (rawReports.next()) |rawReport| {
        var rawLevels = std.mem.tokenizeScalar(u8, rawReport, ' ');
        var previousLevel = try std.fmt.parseUnsigned(i16, rawLevels.next() orelse "0", 10);

        var levelIncreased = false;
        var levelDecreased = false;

        while (rawLevels.next()) |rawLevel| {
            const level = try std.fmt.parseUnsigned(i16, rawLevel, 10);

            const levelChange = level - previousLevel;
            previousLevel = level;

            if (@abs(levelChange) < 1 or @abs(levelChange) > 3) {
                break;
            }

            if (levelChange > 0) {
                levelIncreased = true;
            } else if (levelChange < 0) {
                levelDecreased = true;
            }

            if (levelIncreased and levelDecreased) {
                break;
            }
        } else {
            safeReports = safeReports + 1;
        }
    }

    std.debug.print("Safe reports: {d}\n", .{safeReports});
}
