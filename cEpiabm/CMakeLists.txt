

cmake_minimum_required(VERSION 3.15)
message(STATUS "Using CMake version ${CMAKE_VERSION}")

project(cEpiabm LANGUAGES CXX VERSION 0.0.2)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Link this 'library' to set the C++ standard / compile-time options requested
include(cmake/ProjectSettings.cmake)
add_library(project_settings INTERFACE)
target_compile_features(project_settings INTERFACE cxx_std_17)

# Link this 'library' to use the warnings specified in CompilerWarnings.cmake
add_library(project_warnings INTERFACE)
include(cmake/CompilerWarnings.cmake)
set_project_warnings(project_warnings)

# Sanitiser options if supported by compiler
include(cmake/Sanitisers.cmake)
enable_sanitisers(project_settings)

# allow for static analysis options
include(cmake/StaticAnalysers.cmake)

option(ENABLE_TESTING "Enable Test Builds" ON)

add_subdirectory(src)

if (ENABLE_TESTING)
    enable_testing()
    add_subdirectory(test)
endif ()

option(MAKE_DOCS "Enable doxygen/sphinx commands" OFF)
if (EXISTS ${CMAKE_SOURCE_DIR}/venv/bin/sphinx-build)
    set(MAKE_DOCS ON)
endif()
if (MAKE_DOCS)
    set(CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake" ${CMAKE_MODULE_PATH})
    add_subdirectory(docs)
endif ()

if (ENABLE_EXAMPLES)
    add_subdirectory(examples)
endif()


add_library(epiabm::epiabm_module ALIAS epiabm_lib)
add_library(epiabm::project_warnings ALIAS project_warnings)
add_library(epiabm::project_settings ALIAS project_settings)
include(GNUInstallDirs)
install(TARGETS epiabm_lib project_warnings project_settings EXPORT epiabm)

install(EXPORT epiabm
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/epiabm
        NAMESPACE epiabm::
        FILE epiabm-runtime.cmake
        COMPONENT epiabm-runtime
)

install(FILES cmake/epiabm-config.cmake
        DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/epiabm
)