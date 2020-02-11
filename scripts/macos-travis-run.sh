set -ex

pip3 install pytest
python3 setup.py build
python3 setup.py develop
python3 -m pytest
