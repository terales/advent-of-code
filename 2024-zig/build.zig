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

    const day_01_exe_mod = b.createModule(.{
        .root_source_file = b.path("src/day_01.zig"),
        .target = target,
        .optimize = optimize,
    });

    //
    // Executables
    //
    day_01_exe_mod.addImport("aoc_utils_lib", lib_mod);

    const exe = b.addExecutable(.{
        .name = "2024-zig",
        .root_module = day_01_exe_mod,
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

    const run_step = b.step("run", "Run the app");
    run_step.dependOn(&run_cmd.step);
}
