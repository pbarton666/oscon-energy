# The set of languages for which implicit dependencies are needed:
SET(CMAKE_DEPENDS_LANGUAGES
  )
# The set of files for implicit dependencies of each language:

# Preprocessor definitions for this target.
SET(CMAKE_TARGET_DEFINITIONS
  "BOOST_NO_WREGEX"
  "HAVE_CONFIG_H"
  "NTA_ASM"
  "NTA_ASSERTIONS_ON"
  "NTA_INTERNAL"
  "NTA_PLATFORM_linux64"
  "NTA_PYTHON_SUPPORT=2.7"
  "NUPIC2"
  )

# Targets to which this target links.
SET(CMAKE_TARGET_LINKED_INFO_FILES
  )

# The include file search paths:
SET(CMAKE_C_TARGET_INCLUDE_PATH
  "../../external/linux64/include"
  "../../external/common/include"
  "../../extensions"
  "../.."
  "."
  "/home/pat/.envs/nupic/lib"
  "/home/pat/.envs/nupic/include/python2.7"
  "../../extensions/core/build/release/include"
  "/home/pat/.envs/nupic/local/lib/python2.7/site-packages/numpy/core/include"
  )
SET(CMAKE_CXX_TARGET_INCLUDE_PATH ${CMAKE_C_TARGET_INCLUDE_PATH})
SET(CMAKE_Fortran_TARGET_INCLUDE_PATH ${CMAKE_C_TARGET_INCLUDE_PATH})
SET(CMAKE_ASM_TARGET_INCLUDE_PATH ${CMAKE_C_TARGET_INCLUDE_PATH})
