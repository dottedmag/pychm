set -ex

export PATH=/c/Python37:/c/Python37/Scripts:$PATH
export CL=-IC:\\Users\\travis\\build\\dottedmag\\pychm\\deps\\chmlib\\src
export LINK=/LIBPATH:C:\\Users\\travis\\build\\dottedmag\\pychm\\deps\\chmlib\\src

pip install --user pytest
python setup.py build
python setup.py develop
python -m pytest
