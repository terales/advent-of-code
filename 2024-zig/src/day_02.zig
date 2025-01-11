const std = @import("std");
const aoc_utils = @import("aoc_utils_lib");

pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    const allocator = arena.allocator();
    defer arena.deinit();

    var safeReports: u16 = 0;
    var safeReportsWithProblemDampener: u16 = 0;

    const content = try aoc_utils.getInputContent(allocator);
    var rawReports = std.mem.tokenizeScalar(u8, content, '\n');

    while (rawReports.next()) |rawReport| {
        var report = std.ArrayList(i16).init(allocator);

        var rawLevels = std.mem.tokenizeScalar(u8, rawReport, ' ');
        while (rawLevels.next()) |rawLevel| {
            const level = try std.fmt.parseUnsigned(i16, rawLevel, 10);
            try report.append(level);
        }

        const analysis = analyzeReport(report);
        if (analysis.isCorrect) {
            safeReports = safeReports + 1;
            safeReportsWithProblemDampener = safeReportsWithProblemDampener + 1;
            continue;
        }

        const hasProblemDampenerHelped = try doesProblemDampenerHelp(allocator, report, analysis.firstBadLevelIndex);
        if (hasProblemDampenerHelped) {
            safeReportsWithProblemDampener = safeReportsWithProblemDampener + 1;
        }
    }

    std.debug.print("Safe reports: {d}\n", .{safeReports});
    std.debug.print("Safe reports thanks to the Problem Dampener: {d}\n", .{safeReportsWithProblemDampener});
}

const ReportAnalysis = struct {
    isCorrect: bool,
    firstBadLevelIndex: usize,
};

fn analyzeReport(report: std.ArrayList(i16)) ReportAnalysis {
    var previousLevel = report.items[0];
    var levelIncreased = false;
    var levelDecreased = false;

    for (report.items[1..], 0..) |level, index| {
        const levelChange = level - previousLevel;
        previousLevel = level;

        if (@abs(levelChange) < 1 or @abs(levelChange) > 3) {
            return ReportAnalysis{
                .isCorrect = false,
                .firstBadLevelIndex = index,
            };
        }

        if (levelChange > 0) {
            levelIncreased = true;
        } else if (levelChange < 0) {
            levelDecreased = true;
        }

        if (levelIncreased and levelDecreased) {
            return ReportAnalysis{
                .isCorrect = false,
                .firstBadLevelIndex = index,
            };
        }
    }

    return ReportAnalysis{
        .isCorrect = true,
        .firstBadLevelIndex = 0,
    };
}

fn doesProblemDampenerHelp(allocator: std.mem.Allocator, report: std.ArrayList(i16), badLevelIndex: usize) !bool {
    const levelsToTryDumping = [3]usize{
        badLevelIndex,
        badLevelIndex + 1,
        badLevelIndex -| 1,
    };

    for (levelsToTryDumping) |indexToDump| {
        const dumpedReportSlice = try std.mem.concat(allocator, i16, &[_][]i16{
            report.items[0..indexToDump],
            report.items[indexToDump + 1 ..],
        });

        const dumpedReport = std.ArrayList(i16).fromOwnedSlice(allocator, dumpedReportSlice);

        const dumpedReportAnalysis = analyzeReport(dumpedReport);
        if (dumpedReportAnalysis.isCorrect) {
            return true;
        }
    }

    return false;
}
