import chm.chm as sut, chm.chmlib as sut_chmlib

def test_openclose():
    f = sut.CHMFile()
    assert f.LoadCHM("tests/integration/example.chm") == 1
    assert f.LoadCHM("tests/integration/example.chm") == 1
    f.CloseCHM()

def test_close():
    f = sut.CHMFile()
    f.CloseCHM()

def test_unicode():
    f = sut.CHMFile()
    assert f.LoadCHM(u"tests/integration/example.chm") == 1
    f.CloseCHM()

def test_missing():
    f = sut.CHMFile()
    assert f.LoadCHM(u"hello.chm") == 0
    f.CloseCHM()
