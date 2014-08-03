from setuptools import setup, Extension

long_description = '''
The chm package provides three modules, chm, chmlib and extra, which provide
access to the API implemented by the C library chmlib and some additional
classes and functions. They are used to access MS-ITSS encoded files -
Compressed Html Help files (.chm).
'''

setup(name="pychm",
      version="0.8.4.1",
      description="Python package to handle CHM files",
      author="Rubens Ramos",
      author_email="rubensr@users.sourceforge.net",
      maintainer="Mikhail Gusarov",
      maintainer_email="dottedmag@dottedmag.net",
      url="https://github.com/dottedmag/pychm",
      license="GPL",
      long_description=long_description,
      py_modules=["chm.chm", "chm.chmlib"],
      ext_modules=[Extension("chm._chmlib",
                             ["chm/swig_chm.c"],
                             libraries=["chm"],
                             extra_compile_args=["-DSWIG_COBJECT_TYPES"]),
                   Extension("chm.extra",
                             ["chm/extra.c"],
                             extra_compile_args=["-D__PYTHON__"],
                             libraries=["chm"])]
      )
