find_package(LLVM REQUIRED CONFIG)

include_directories(${LLVM_INCLUDE_DIRS})
separate_arguments(LLVM_DEFINITIONS_LIST NATIVE_COMMAND ${LLVM_DEFINITIONS})
add_definitions(${LLVM_DEFINITIONS_LIST})

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_executable(${TARGET} ${SOURCE})

llvm_map_components_to_libnames(llvm_libs support core irreader)
target_link_libraries(${TARGET} ${llvm_libs})

target_compile_options(${TARGET} PRIVATE -stdlib=libc++)
target_link_options(${TARGET} PRIVATE -stdlib=libc++)
