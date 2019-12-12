set -ex

dl_chmlib() {
  rm -rf deps && mkdir -p deps
  # chmlib 0.40
  wget -O deps/chmlib-0.40.tar.gz http://www.jedrea.com/chmlib/chmlib-0.40.tar.gz
  tar -C deps -xf deps/chmlib-0.40.tar.gz
  mv deps/chmlib-0.40 deps/chmlib
}

build_chmlib() {
  cmd.exe /C scripts\\build-chmlib.bat
}

dl_chmlib
build_chmlib

choco install python --version 3.7.5
