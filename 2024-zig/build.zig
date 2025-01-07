const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    //
    // Libraries
    //
    const lib_mod = b.createModule(.{
        .root_source_file = b.path("src/aoc_utils.zig"),
        .target = target,
        .optimize = optimize,
    });

    const lib = b.addStaticLibrary(.{
        .name = "aoc_utils",
        .root_module = lib_mod,
    });

    b.installArtifact(lib);

    //
    // Executables
    //
    const src = "src";
    const day_root_start = "day";

    var dir = std.fs.cwd().openDir(src, .{ .iterate = true }) catch unreachable;
    defer dir.close();
    var dir_iterator = dir.iterate();

    while (dir_iterator.next() catch unreachable) |entry| {
        if (entry.kind != .file or !std.mem.startsWith(u8, entry.name, day_root_start)) {
            continue;
        }

        const exe_mod = b.createModule(.{
            .root_source_file = .{
                .src_path = .{
                    .sub_path = b.pathJoin(&.{ src, entry.name }),
                    .owner = b,
                },
            },
            .target = target,
            .optimize = optimize,
        });

        exe_mod.addImport("aoc_utils_lib", lib_mod);

        const exe = b.addExecutable(.{
            .name = std.fs.path.stem(entry.name),
            .root_module = exe_mod,
        });

        b.installArtifact(exe);

        //
        // Run step
        //
        const run_cmd = b.addRunArtifact(exe);
        run_cmd.step.dependOn(b.getInstallStep());

        if (b.args) |args| {
            run_cmd.addArgs(args);
        }

        const step_name = b.fmt("run_{s}", .{std.fs.path.stem(entry.name)});
        const run_step = b.step(step_name, "Run the day's solution");
        run_step.dependOn(&run_cmd.step);
    }
}
