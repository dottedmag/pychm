import chm.chm as sut, chm.chmlib as sut_chmlib

def test_crash_in_callback():
    """
    Test checks that an exception in a callback does not cause a crash in
    chmlib module.
    """
    f = sut.CHMFile()
    f.LoadCHM("tests/integration/example.chm")

    def enumerator(chm_file, ui, context):
        1/0

    try:
        sut_chmlib.chm_enumerate(f.file, sut_chmlib.CHM_ENUMERATE_NORMAL, enumerator, None)
    except ZeroDivisionError:
        pass

    f.CloseCHM()

def test_enumerate():
    f = sut.CHMFile()
    f.LoadCHM("tests/integration/example.chm")

    ret = []

    def enumerator(chm_file, ui, context):
        ret.append(ui.path)

    sut_chmlib.chm_enumerate(f.file, sut_chmlib.CHM_ENUMERATE_NORMAL, enumerator, None)

    f.CloseCHM()

    assert ret == [
        b'/',
        b'/Documents/',
        b'/Documents/Table of Contents.hhc',
        b'/page 1.html',
        b'/page 2.html',
    ]

def test_enumerate_dir():
    f = sut.CHMFile()
    f.LoadCHM("tests/integration/example.chm")

    ret = []

    def enumerator(chm_file, ui, context):
        ret.append(ui.path)

    sut_chmlib.chm_enumerate_dir(f.file, b'/Documents/',
                                 sut_chmlib.CHM_ENUMERATE_NORMAL, enumerator,
                                 None)

    f.CloseCHM()

    assert ret == [b'/Documents/Table of Contents.hhc']
