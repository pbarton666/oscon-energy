# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 2.8

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list

# Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/pat/workspace/nupic

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/pat/workspace/nupic/build/scripts

# Include any dependencies generated for this target.
include CMakeFiles/compare_nupic_core_version.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/compare_nupic_core_version.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/compare_nupic_core_version.dir/flags.make

CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o: CMakeFiles/compare_nupic_core_version.dir/flags.make
CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o: ../../extensions/compare_nupic_core_version.cpp
	$(CMAKE_COMMAND) -E cmake_progress_report /home/pat/workspace/nupic/build/scripts/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Building CXX object CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o"
	/usr/bin/c++   $(CXX_DEFINES) $(CXX_FLAGS) -o CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o -c /home/pat/workspace/nupic/extensions/compare_nupic_core_version.cpp

CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.i"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -E /home/pat/workspace/nupic/extensions/compare_nupic_core_version.cpp > CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.i

CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.s"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_FLAGS) -S /home/pat/workspace/nupic/extensions/compare_nupic_core_version.cpp -o CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.s

CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o.requires:
.PHONY : CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o.requires

CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o.provides: CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o.requires
	$(MAKE) -f CMakeFiles/compare_nupic_core_version.dir/build.make CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o.provides.build
.PHONY : CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o.provides

CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o.provides.build: CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o

# Object files for target compare_nupic_core_version
compare_nupic_core_version_OBJECTS = \
"CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o"

# External object files for target compare_nupic_core_version
compare_nupic_core_version_EXTERNAL_OBJECTS =

compare_nupic_core_version: CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o
compare_nupic_core_version: CMakeFiles/compare_nupic_core_version.dir/build.make
compare_nupic_core_version: CMakeFiles/compare_nupic_core_version.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --red --bold "Linking CXX executable compare_nupic_core_version"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/compare_nupic_core_version.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/compare_nupic_core_version.dir/build: compare_nupic_core_version
.PHONY : CMakeFiles/compare_nupic_core_version.dir/build

CMakeFiles/compare_nupic_core_version.dir/requires: CMakeFiles/compare_nupic_core_version.dir/extensions/compare_nupic_core_version.cpp.o.requires
.PHONY : CMakeFiles/compare_nupic_core_version.dir/requires

CMakeFiles/compare_nupic_core_version.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/compare_nupic_core_version.dir/cmake_clean.cmake
.PHONY : CMakeFiles/compare_nupic_core_version.dir/clean

CMakeFiles/compare_nupic_core_version.dir/depend:
	cd /home/pat/workspace/nupic/build/scripts && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pat/workspace/nupic /home/pat/workspace/nupic /home/pat/workspace/nupic/build/scripts /home/pat/workspace/nupic/build/scripts /home/pat/workspace/nupic/build/scripts/CMakeFiles/compare_nupic_core_version.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/compare_nupic_core_version.dir/depend

