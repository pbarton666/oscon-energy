FILE(REMOVE_RECURSE
  "../../temp/extensions/bindings/py/engine_internal/EngineInternalPyPYTHON_wrap.cxx"
  "../../temp/EngineInternalPy.py"
  "../../temp/extensions/bindings/py/math/MathPyPYTHON_wrap.cxx"
  "../../temp/MathPy.py"
  "../../temp/extensions/bindings/py/algorithms/AlgorithmsPyPYTHON_wrap.cxx"
  "../../temp/AlgorithmsPy.py"
  "../../temp/extensions/bindings/py/iorange/IorangePyPYTHON_wrap.cxx"
  "../../temp/IorangePy.py"
  "CMakeFiles/python_unit_tests"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/python_unit_tests.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
