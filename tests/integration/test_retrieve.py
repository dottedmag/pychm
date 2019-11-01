import chm.chm as sut

def test_retrieve_closed():
    f = sut.CHMFile()
    assert f.RetrieveObject(1, 0, 100) == (0, b'')

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

def test_retrieve_size_offset():
    f = sut.CHMFile()
    f.LoadCHM("tests/integration/example.chm")

    succ, ui = f.ResolveObject(b'/page 1.html')

    (size, content) = f.RetrieveObject(ui, 99)
    assert size == 71
    assert content.startswith('head>')

    assert f.RetrieveObject(ui, 99, 10) == (10, 'head>\n  <t')

def test_retrieve_overlong():
    f = sut.CHMFile()
    f.LoadCHM("tests/integration/example.chm")

    succ, ui = f.ResolveObject(b'/page 1.html')

    assert f.RetrieveObject(ui, 10, 170) == (0, b'')
