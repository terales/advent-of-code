set(RULE_MESSAGES OFF)
set(CMAKE_RULE_MESSAGES OFF)
set(CMAKE_TARGET_MESSAGES OFF)
set(CMAKE_INSTALL_MESSAGE NEVER)
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


add_executable(${TARGET} ${SOURCE})


add_library(AocUtilsModule 
    "${CMAKE_CURRENT_LIST_DIR}/_utils/aoc_common.cpp"
)

include_directories(${TARGET}
    "${CMAKE_CURRENT_LIST_DIR}/_utils"
)

find_package(LLVM REQUIRED CONFIG)
find_package(Boost 1.87.0 EXACT)

include_directories(${TARGET} SYSTEM
    ${Boost_INCLUDE_DIRS}
    ${LLVM_INCLUDE_DIRS}
)
separate_arguments(LLVM_DEFINITIONS_LIST NATIVE_COMMAND ${LLVM_DEFINITIONS})
add_definitions(${LLVM_DEFINITIONS_LIST})

llvm_map_components_to_libnames(llvm_libs support core irreader)
target_link_libraries(AocUtilsModule ${llvm_libs})


target_link_libraries(${TARGET} AocUtilsModule)
target_compile_options(${TARGET} PRIVATE -stdlib=libc++)
target_link_options(${TARGET} PRIVATE -stdlib=libc++)
