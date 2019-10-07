import chm.chm as sut, chm.chmlib as sut_chmlib

def test_error_in_callback():
    f = sut.CHMFile()
    f.LoadCHM("tests/integration/example.chm")

    def enumerator(chm_file, ui, context):
        1/0

    sut_chmlib.chm_enumerate(f.file, sut_chmlib.CHM_ENUMERATE_NORMAL, enumerator, None)

    f.CloseCHM()
