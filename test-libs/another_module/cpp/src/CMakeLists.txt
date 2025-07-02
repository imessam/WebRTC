cmake_minimum_required(VERSION 3.15...3.31)

project(AnotherModule VERSION 1.0
                  DESCRIPTION "Another Module"
                  LANGUAGES CXX)

## Libraries setup

set(ANOTHER_MODULE_SOURCES

)

if (NOT TARGET AnotherModuleLib)

#   include(${CMAKE_CURRENT_LIST_DIR}/../../libs/CMakeLists.txt)

  add_library(AnotherModuleLib STATIC ${ANOTHER_MODULE_SOURCES})

  target_include_directories(AnotherModuleLib PUBLIC ${CMAKE_CURRENT_LIST_DIR}/../include)

#   foreach(_lib_include_dir
#   ${libs_include_another_module})
#   target_include_directories(AnotherModuleLib PUBLIC
#         ${_lib_include_dir}
#       )
#   endforeach()

endif()
