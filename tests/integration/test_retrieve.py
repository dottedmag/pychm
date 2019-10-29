import chm.chm as sut

def _test_file(f, filename, exp_size, exp_start):
    succ, ui = f.ResolveObject(filename)
    assert succ == 0

    (size, content) = f.RetrieveObject(ui)
    assert size == exp_size
    assert content.startswith(exp_start)


def test_retrieve():
    f = sut.CHMFile()
    f.LoadCHM("tests/integration/example.chm")

    tt = f.GetTopicsTree()
    assert tt.startswith(b'<!DOCTYPE')

    assert f.GetIndex() is None
    assert f.GetLCID() == (b'iso8859_1', b'Norwegian_Bokmal', b'Western Europe & US')
    assert f.GetEncoding() is None
    assert f.IsSearchable() == True

    _test_file(f, b'/Documents/Table of Contents.hhc', 566, b'<!DOCTYPE')
    _test_file(f, b'/page 1.html', 170, b'<!DOCTYPE')
    _test_file(f, b'/page 2.html', 181, b'<!DOCTYPE')

    f.CloseCHM()
