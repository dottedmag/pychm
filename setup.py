from setuptools import setup, Extension

with open("README", "r") as fh:
    long_description = fh.read()

setup(name="pychm",
      version="0.8.5",
      description="Python package to handle CHM files",
      author="Rubens Ramos",
      author_email="rubensr@users.sourceforge.net",
      maintainer="Mikhail Gusarov",
      maintainer_email="dottedmag@dottedmag.net",
      url="https://github.com/dottedmag/pychm",
      license="GPL",
      long_description=long_description,
      py_modules=["chm.chm", "chm.chmlib", "chm.extra"],
      ext_modules=[Extension("chm._chmlib", ["chm/_chmlib.c", "chm/search.c"],
                             libraries=["chm"])])
