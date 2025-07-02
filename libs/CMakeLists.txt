cmake_minimum_required(VERSION 3.15...3.31)

project(MyModuleSubmodules VERSION 1.0
                  DESCRIPTION "My Module Submodules"
                  LANGUAGES CXX)

set(libs_include_my_module
    ${CMAKE_CURRENT_LIST_DIR}/another_module/cpp/include
)

include(${CMAKE_CURRENT_LIST_DIR}/another_module/cpp/src/CMakeLists.txt)

set(libs_targets_my_module

    AnotherModuleLib
)

