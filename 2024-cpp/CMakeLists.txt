cmake_minimum_required(VERSION 3.31.3)

project(CppAdventOfCode2024)

find_package(LLVM REQUIRED CONFIG)

include_directories(${LLVM_INCLUDE_DIRS})
separate_arguments(LLVM_DEFINITIONS_LIST NATIVE_COMMAND ${LLVM_DEFINITIONS})
add_definitions(${LLVM_DEFINITIONS_LIST})

message(STATUS "Found LLVM ${LLVM_PACKAGE_VERSION}")
message(STATUS "Using LLVMConfig.cmake in: ${LLVM_DIR}")

cmake_minimum_required(VERSION 3.31)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

file(GLOB_RECURSE CPP_FILES "${CMAKE_CURRENT_SOURCE_DIR}/[0-9][0-9]/*.cpp")

foreach(CPP_FILE ${CPP_FILES})
    get_filename_component(SOURCE_FILE_NAME ${CPP_FILE} NAME_WE)
    get_filename_component(SOURCE_DIR ${CPP_FILE} DIRECTORY)

    add_executable(${SOURCE_FILE_NAME} ${CPP_FILE})

    llvm_map_components_to_libnames(llvm_libs support core irreader)
    target_link_libraries(${SOURCE_FILE_NAME} ${llvm_libs})

    target_compile_options(${SOURCE_FILE_NAME} PRIVATE -stdlib=libc++)
    target_link_options(${SOURCE_FILE_NAME} PRIVATE -stdlib=libc++)

    set_target_properties(
        ${SOURCE_FILE_NAME} PROPERTIES
        RUNTIME_OUTPUT_DIRECTORY "${SOURCE_DIR}"
        SUFFIX "-bin"
    )
endforeach()
