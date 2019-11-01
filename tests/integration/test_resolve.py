import chm.chm as sut, chm.chmlib as sut_chmlib

def test_resolve_closed():
    f = sut.CHMFile()
    assert f.ResolveObject("Something") == (1, None)
