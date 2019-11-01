import chm.chm as sut, chm.chmlib as sut_chmlib

def test_search():
    f = sut.CHMFile()
    f.LoadCHM("tests/integration/example.chm")

    (partial, results) = f.Search(b'page')

    assert partial == 1
    assert len(results) == 1
    assert results[b'Untitled in index'] == b'page 2.html'

    f.CloseCHM()

def test_search_closed():
    f = sut.CHMFile()
    assert f.Search(b'hello') == None

def test_search_none():
    f = sut.CHMFile()
    assert f.Search(None) == None

def test_search_empty():
    f = sut.CHMFile()
    assert f.Search(b'') == None
