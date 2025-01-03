project(CppAdventOfCode2024)

set(CMAKE_C_COMPILER "/opt/homebrew/opt/llvm/bin/clang")
set(CMAKE_CXX_COMPILER "/opt/homebrew/opt/llvm/bin/clang++")

cmake_minimum_required(VERSION 3.31)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

file(GLOB_RECURSE CPP_FILES "${CMAKE_CURRENT_SOURCE_DIR}/[0-9][0-9]/*.cpp")

foreach(CPP_FILE ${CPP_FILES})
    get_filename_component(SOURCE_FILE_NAME ${CPP_FILE} NAME_WE)
    get_filename_component(SOURCE_DIR ${CPP_FILE} DIRECTORY)

    add_executable(${SOURCE_FILE_NAME} ${CPP_FILE})

    target_compile_options(${SOURCE_FILE_NAME} PRIVATE -stdlib=libc++)
    target_link_options(${SOURCE_FILE_NAME} PRIVATE -stdlib=libc++)

    set_target_properties(
        ${SOURCE_FILE_NAME} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY "${SOURCE_DIR}"
        SUFFIX "-bin"
    )
endforeach()
