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

    var leftList = std.ArrayList(u8).init(allocator);
    defer leftList.deinit();
    var rightList = std.ArrayList(u8).init(allocator);
    defer rightList.deinit();
    var rightListOccurrences = std.AutoHashMap(u8, u8).init(allocator);
    defer rightListOccurrences.deinit();

    var isEven = true;

    while (splitSequence.next()) |token| {
        const tokenInt = try std.fmt.parseInt(u8, token, 10);

        if (isEven) {
            try leftList.append(tokenInt);
        } else {
            try rightList.append(tokenInt);

            const occurrences = rightListOccurrences.get(tokenInt) orelse 0;
            try rightListOccurrences.put(tokenInt, occurrences + 1);
        }
        isEven = !isEven;
    }

    std.mem.sort(u8, leftList.items, {}, std.sort.asc(u8));
    std.mem.sort(u8, rightList.items, {}, std.sort.asc(u8));

    var totalDistance: u16 = 0;
    var similarityScore: u16 = 0;
    for (leftList.items, 0..) |leftItem, i| {
        totalDistance += @abs(@as(i16, leftItem) - @as(i16, rightList.items[i]));
        similarityScore += leftItem * (rightListOccurrences.get(leftItem) orelse 0);
    }

    std.debug.print("Total distance: {d}\n", .{totalDistance});
    std.debug.print("Similarity score: {d}\n", .{similarityScore});
}
