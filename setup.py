import distutils
from distutils.core import setup, Extension

setup(name="pychm",
      version="0.5.0",
      description="Python package to handle CHM files",
      author="Rubens Ramos",
      author_email="rubensr@users.sourceforge.net",
      url="http://gnochm.sourceforge.net",
      license="GPL",
      long_description="The chm package provides two modules, chm and chmlib, which provide access to the API implemented by the C library chmlib. This is used to access MS-ITSS encoded files - Microsoft Html Help files (.chm).",
      py_modules = ["chm.chm", "chm.chmlib"],
      ext_modules = [Extension("chm._chmlib",
                               ["chm/swig_chm.c"],
                               libraries=["chm"],
                               )]
      )
