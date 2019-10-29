import chm.chm as sut, chm.chmlib as sut_chmlib

def test_search():
    f = sut.CHMFile()
    f.LoadCHM("tests/integration/example.chm")

    (partial, results) = f.Search("page")

    assert partial == 1
    assert len(results) == 1
    assert results["Untitled in index"] == "page 2.html"

    f.CloseCHM()
