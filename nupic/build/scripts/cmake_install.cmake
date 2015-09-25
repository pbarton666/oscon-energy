# Install script for directory: /home/pat/workspace/nupic

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/home/pat/workspace/nupic")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

# Install shared libraries without execute permission?
IF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  SET(CMAKE_INSTALL_SO_NO_EXE "1")
ENDIF(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  IF(EXISTS "$ENV{DESTDIR}/home/pat/workspace/nupic/bin/testpyhtm" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/pat/workspace/nupic/bin/testpyhtm")
    FILE(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/pat/workspace/nupic/bin/testpyhtm"
         RPATH "")
  ENDIF()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/pat/workspace/nupic/bin/testpyhtm")
  IF (CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  ENDIF (CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
  IF (CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  ENDIF (CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
FILE(INSTALL DESTINATION "/home/pat/workspace/nupic/bin" TYPE EXECUTABLE FILES "/home/pat/workspace/nupic/build/scripts/testpyhtm")
  IF(EXISTS "$ENV{DESTDIR}/home/pat/workspace/nupic/bin/testpyhtm" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/pat/workspace/nupic/bin/testpyhtm")
    IF(CMAKE_INSTALL_DO_STRIP)
      EXECUTE_PROCESS(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/home/pat/workspace/nupic/bin/testpyhtm")
    ENDIF(CMAKE_INSTALL_DO_STRIP)
  ENDIF()
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  IF(EXISTS "$ENV{DESTDIR}/home/pat/workspace/nupic/nupic/libcpp_region.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/pat/workspace/nupic/nupic/libcpp_region.so")
    FILE(RPATH_CHECK
         FILE "$ENV{DESTDIR}/home/pat/workspace/nupic/nupic/libcpp_region.so"
         RPATH "")
  ENDIF()
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/pat/workspace/nupic/nupic/libcpp_region.so")
  IF (CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  ENDIF (CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
  IF (CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  ENDIF (CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
FILE(INSTALL DESTINATION "/home/pat/workspace/nupic/nupic" TYPE SHARED_LIBRARY FILES "/home/pat/workspace/nupic/build/scripts/libcpp_region.so")
  IF(EXISTS "$ENV{DESTDIR}/home/pat/workspace/nupic/nupic/libcpp_region.so" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}/home/pat/workspace/nupic/nupic/libcpp_region.so")
    IF(CMAKE_INSTALL_DO_STRIP)
      EXECUTE_PROCESS(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}/home/pat/workspace/nupic/nupic/libcpp_region.so")
    ENDIF(CMAKE_INSTALL_DO_STRIP)
  ENDIF()
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/home/pat/workspace/nupic/nupic/bindings/_engine_internal.so;/home/pat/workspace/nupic/nupic/bindings/engine_internal.py;/home/pat/workspace/nupic/nupic/bindings/_math.so;/home/pat/workspace/nupic/nupic/bindings/math.py;/home/pat/workspace/nupic/nupic/bindings/_algorithms.so;/home/pat/workspace/nupic/nupic/bindings/algorithms.py;/home/pat/workspace/nupic/nupic/bindings/_iorange.so;/home/pat/workspace/nupic/nupic/bindings/iorange.py")
  IF (CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  ENDIF (CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
  IF (CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  ENDIF (CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
FILE(INSTALL DESTINATION "/home/pat/workspace/nupic/nupic/bindings" TYPE FILE FILES
    "/home/pat/workspace/nupic/build/scripts/_engine_internal.so"
    "/home/pat/workspace/nupic/temp/engine_internal.py"
    "/home/pat/workspace/nupic/build/scripts/_math.so"
    "/home/pat/workspace/nupic/temp/math.py"
    "/home/pat/workspace/nupic/build/scripts/_algorithms.so"
    "/home/pat/workspace/nupic/temp/algorithms.py"
    "/home/pat/workspace/nupic/build/scripts/_iorange.so"
    "/home/pat/workspace/nupic/temp/iorange.py"
    )
ENDIF(NOT CMAKE_INSTALL_COMPONENT OR "${CMAKE_INSTALL_COMPONENT}" STREQUAL "Unspecified")

IF(CMAKE_INSTALL_COMPONENT)
  SET(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
ELSE(CMAKE_INSTALL_COMPONENT)
  SET(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
ENDIF(CMAKE_INSTALL_COMPONENT)

FILE(WRITE "/home/pat/workspace/nupic/build/scripts/${CMAKE_INSTALL_MANIFEST}" "")
FOREACH(file ${CMAKE_INSTALL_MANIFEST_FILES})
  FILE(APPEND "/home/pat/workspace/nupic/build/scripts/${CMAKE_INSTALL_MANIFEST}" "${file}\n")
ENDFOREACH(file)
