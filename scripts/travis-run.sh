set -ex

pip install pytest
python setup.py build
python setup.py develop
python -m pytest
