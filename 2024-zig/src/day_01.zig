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

    var leftList = std.ArrayList(u32).init(allocator);
    defer leftList.deinit();
    var rightList = std.ArrayList(u32).init(allocator);
    defer rightList.deinit();
    var rightListOccurrences = std.AutoHashMap(u32, u32).init(allocator);
    defer rightListOccurrences.deinit();

    var isEven = true;

    while (splitSequence.next()) |token| {
        const tokenInt = try std.fmt.parseUnsigned(u32, token, 10);

        if (isEven) {
            try leftList.append(tokenInt);
        } else {
            try rightList.append(tokenInt);

            const occurrences = rightListOccurrences.get(tokenInt) orelse 0;
            try rightListOccurrences.put(tokenInt, occurrences + 1);
        }
        isEven = !isEven;
    }

    std.mem.sort(u32, leftList.items, {}, std.sort.asc(u32));
    std.mem.sort(u32, rightList.items, {}, std.sort.asc(u32));

    var totalDistance: u64 = 0;
    var similarityScore: u64 = 0;
    for (leftList.items, 0..) |leftItem, i| {
        totalDistance += @abs(@as(i64, leftItem) - @as(i64, rightList.items[i]));
        similarityScore += leftItem * (rightListOccurrences.get(leftItem) orelse 0);
    }

    std.debug.print("Total distance: {d}\n", .{totalDistance});
    std.debug.print("Similarity score: {d}\n", .{similarityScore});
}
