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

    sut_chmlib.chm_enumerate(f.file, sut_chmlib.CHM_ENUMERATE_NORMAL, enumerator, None)

    f.CloseCHM()
