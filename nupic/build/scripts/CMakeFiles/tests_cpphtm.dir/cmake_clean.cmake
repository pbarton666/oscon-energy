FILE(REMOVE_RECURSE
  "../../temp/extensions/bindings/py/engine_internal/EngineInternalPyPYTHON_wrap.cxx"
  "../../temp/EngineInternalPy.py"
  "../../temp/extensions/bindings/py/math/MathPyPYTHON_wrap.cxx"
  "../../temp/MathPy.py"
  "../../temp/extensions/bindings/py/algorithms/AlgorithmsPyPYTHON_wrap.cxx"
  "../../temp/AlgorithmsPy.py"
  "../../temp/extensions/bindings/py/iorange/IorangePyPYTHON_wrap.cxx"
  "../../temp/IorangePy.py"
  "CMakeFiles/tests_cpphtm"
)

# Per-language clean rules from dependency scanning.
FOREACH(lang)
  INCLUDE(CMakeFiles/tests_cpphtm.dir/cmake_clean_${lang}.cmake OPTIONAL)
ENDFOREACH(lang)
