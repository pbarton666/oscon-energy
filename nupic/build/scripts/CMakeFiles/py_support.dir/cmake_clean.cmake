FILE(REMOVE_RECURSE
  "../../temp/extensions/bindings/py/engine_internal/EngineInternalPyPYTHON_wrap.cxx"
  "../../temp/EngineInternalPy.py"
  "../../temp/extensions/bindings/py/math/MathPyPYTHON_wrap.cxx"
  "../../temp/MathPy.py"
  "../../temp/extensions/bindings/py/algorithms/AlgorithmsPyPYTHON_wrap.cxx"
  "../../temp/AlgorithmsPy.py"
  "../../temp/extensions/bindings/py/iorange/IorangePyPYTHON_wrap.cxx"
  "../../temp/IorangePy.py"
  "CMakeFiles/py_support.dir/extensions/py_support/NumpyVector.cpp.o"
  "CMakeFiles/py_support.dir/extensions/py_support/PyArray.cpp.o"
  "CMakeFiles/py_support.dir/extensions/py_support/PyHelpers.cpp.o"
  "CMakeFiles/py_support.dir/extensions/py_support/PythonStream.cpp.o"
  "libpy_support.pdb"
  "libpy_support.a"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang CXX)
  INCLUDE(CMakeFiles/py_support.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
