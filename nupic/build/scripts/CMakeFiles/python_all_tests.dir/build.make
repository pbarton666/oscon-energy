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

# Utility rule file for python_all_tests.

# Include the progress variables for this target.
include CMakeFiles/python_all_tests.dir/progress.make

CMakeFiles/python_all_tests:
	$(CMAKE_COMMAND) -E cmake_progress_report /home/pat/workspace/nupic/build/scripts/CMakeFiles $(CMAKE_PROGRESS_1)
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold "Python tests + integration + swarming (requires DB)"
	python /home/pat/workspace/nupic/scripts/run_tests.py --all --coverage

python_all_tests: CMakeFiles/python_all_tests
python_all_tests: CMakeFiles/python_all_tests.dir/build.make
.PHONY : python_all_tests

# Rule to build all files generated by this target.
CMakeFiles/python_all_tests.dir/build: python_all_tests
.PHONY : CMakeFiles/python_all_tests.dir/build

CMakeFiles/python_all_tests.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/python_all_tests.dir/cmake_clean.cmake
.PHONY : CMakeFiles/python_all_tests.dir/clean

CMakeFiles/python_all_tests.dir/depend:
	cd /home/pat/workspace/nupic/build/scripts && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/pat/workspace/nupic /home/pat/workspace/nupic /home/pat/workspace/nupic/build/scripts /home/pat/workspace/nupic/build/scripts /home/pat/workspace/nupic/build/scripts/CMakeFiles/python_all_tests.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/python_all_tests.dir/depend

