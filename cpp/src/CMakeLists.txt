cmake_minimum_required(VERSION 3.15...3.31)

project(MyModule VERSION 1.0
                  DESCRIPTION "My Module"
                  LANGUAGES CXX)

## Libraries setup

set(MY_MODULE_SOURCES

  ${CMAKE_CURRENT_LIST_DIR}/class_abstract_base.cpp

  ${CMAKE_CURRENT_LIST_DIR}/class_implemented_derived.cpp

)

if (NOT TARGET MyModuleLib)

  include(${CMAKE_CURRENT_LIST_DIR}/../../libs/CMakeLists.txt)

  add_library(MyModuleLib STATIC ${MY_MODULE_SOURCES})

  target_include_directories(MyModuleLib PUBLIC ${CMAKE_CURRENT_LIST_DIR}/../include)

  foreach(_lib_include_dir
  ${libs_include_my_module})
  target_include_directories(MyModuleLib PUBLIC
        ${_lib_include_dir}
      )
  endforeach()

endif()
