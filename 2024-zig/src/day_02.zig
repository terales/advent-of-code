const std = @import("std");
const aoc_utils = @import("aoc_utils_lib");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    const allocator = arena.allocator();
    defer arena.deinit();

    var safeReports: u16 = 0;
    var safeReportsWithProblemDampener: u16 = 0;

    for (try getParsedInput(allocator)) |report| {
        const unsafeLevelIndex = findUnsafeLevel(report);
        if (unsafeLevelIndex == null) {
            safeReports = safeReports + 1;
            safeReportsWithProblemDampener = safeReportsWithProblemDampener + 1;
            continue;
        }

        const hasProblemDampenerHelped = try doesProblemDampenerHelp(allocator, report, unsafeLevelIndex.?);
        if (hasProblemDampenerHelped) {
            safeReportsWithProblemDampener = safeReportsWithProblemDampener + 1;
        }
    }

    std.debug.print("Safe reports: {d}\n", .{safeReports});
    std.debug.print("Safe reports thanks to the Problem Dampener: {d}\n", .{safeReportsWithProblemDampener});
}

fn getParsedInput(allocator: std.mem.Allocator) ![][]i16 {
    var reports = std.ArrayList([]i16).init(allocator);

    const content = try aoc_utils.getInputContent(allocator);
    var rawReports = std.mem.tokenizeScalar(u8, content, '\n');

    while (rawReports.next()) |rawReport| {
        var report = std.ArrayList(i16).init(allocator);

        var rawLevels = std.mem.tokenizeScalar(u8, rawReport, ' ');
        while (rawLevels.next()) |rawLevel| {
            const level = try std.fmt.parseUnsigned(i16, rawLevel, 10);
            try report.append(level);
        }
        try reports.append(report.items);
    }

    return reports.items;
}

fn findUnsafeLevel(report: []i16) ?usize {
    var levelIncreased = false;
    var levelDecreased = false;

    for (report[1..], 1..) |level, index| {
        const previousLevel = report[index - 1];
        const levelChange = level - previousLevel;

        if (@abs(levelChange) < 1 or @abs(levelChange) > 3) {
            return index;
        }

        if (levelChange > 0) {
            levelIncreased = true;
        } else if (levelChange < 0) {
            levelDecreased = true;
        }

        if (levelIncreased and levelDecreased) {
            return index;
        }
    }

    return null;
}

fn doesProblemDampenerHelp(allocator: std.mem.Allocator, report: []i16, badLevelIndex: usize) !bool {
    const levelsToTryDumping = [_]usize{
        badLevelIndex -| 2,
        badLevelIndex -| 1,
        badLevelIndex,
    };

    for (levelsToTryDumping) |indexToDump| {
        const dumpedReport = try std.mem.concat(allocator, i16, &[_][]i16{
            report[0..indexToDump],
            report[indexToDump + 1 ..],
        });

        const unsafeLevelIndex = findUnsafeLevel(dumpedReport);
        if (unsafeLevelIndex == null) {
            return true;
        }
    }

    return false;
}
