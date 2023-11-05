import chm.chm as sut

PATH1 = 'tests/integration/combined.chm'
PATH2 = 'tests/integration/combined2.chm'

# combined.chm contains /Untitled1.htm, /Untitled2.htm, an Index, and no TOC.
# combined2.chm contains /Untitled2.htm, a TOC, and no Index.

def test_duplicate_object1():
    '''Verify the last file's version of a duplicate object is used.'''
    collection = sut.CHMCollection()
    assert collection.LoadFiles(PATH1, PATH2) == 1
    res1, ui1, file1 = collection.ResolveObject(b'/Untitled1.htm')
    res2, ui2, file2 = collection.ResolveObject(b'/Untitled2.htm')
    assert res1 == 0
    assert file1 == collection.files[0]
    assert res2 == 0
    assert file2 == collection.files[1]
    size1, content1 = file1.RetrieveObject(ui1)
    size2, content2 = file2.RetrieveObject(ui2)
    assert size1 == 211
    assert 'Hello, world' in content1.decode()
    assert size2 == 199
    assert 'Two' in content2.decode()

def test_duplicate_object2():
    '''Verify the last file's version of a duplicate object is used,
    while not affecting the result of a nonduplicate object.
    '''
    collection = sut.CHMCollection()
    assert collection.LoadFiles(PATH2, PATH1) == 1
    res1, ui1, file1 = collection.ResolveObject(b'/Untitled1.htm')
    res2, ui2, file2 = collection.ResolveObject(b'/Untitled2.htm')
    assert res1 == 0
    assert file1 == collection.files[1]
    assert res2 == 0
    assert file2 == collection.files[1]
    size1, content1 = file1.RetrieveObject(ui1)
    size2, content2 = file2.RetrieveObject(ui2)
    assert size1 == 211
    assert 'Hello, world' in content1.decode()
    assert size2 == 199
    assert 'Two' in content2.decode()

def test_resolve1():
    '''Verify nonduplicate objects are correctly resolved regardless
    of load order.'''
    collection = sut.CHMCollection()
    assert collection.LoadFiles(PATH1, PATH2) == 1
    res1, ui1, file1 = collection.ResolveObject(b'/Index.hhk')
    res2, ui2, file2 = collection.ResolveObject(b'/Table of Contents2.hhc')
    res3, _, file3 = collection.ResolveObject(b'/does not exist.hhk')
    assert res1 == 0
    assert file1 == collection.files[0]
    assert res2 == 0
    assert file2 == collection.files[1]
    assert res3 == 1
    assert file3 == None
    size1, content1 = file1.RetrieveObject(ui1)
    size2, content2 = file2.RetrieveObject(ui2)
    assert size1 == 464
    assert 'Untitled1.htm' in content1.decode()
    assert size2 == 424
    assert 'Untitled2.htm' in content2.decode()

def test_resolve2():
    '''Verify nonduplicate objects are correctly resolved regardless
    of load order.'''
    collection = sut.CHMCollection()
    assert collection.LoadFiles(PATH2, PATH1) == 1
    res1, ui1, file1 = collection.ResolveObject(b'/Index.hhk')
    res2, ui2, file2 = collection.ResolveObject(b'/Table of Contents2.hhc')
    res3, _, file3 = collection.ResolveObject(b'/does not exist.hhk')
    assert res1 == 0
    assert file1 == collection.files[1]
    assert res2 == 0
    assert file2 == collection.files[0]
    assert res3 == 1
    assert file3 == None
    size1, content1 = file1.RetrieveObject(ui1)
    size2, content2 = file2.RetrieveObject(ui2)
    assert size1 == 464
    assert 'Untitled1.htm' in content1.decode()
    assert size2 == 424
    assert 'Untitled2.htm' in content2.decode()

def test_topics1():
    '''Verify the topics tree is returned regardless of load order.'''
    collection = sut.CHMCollection()
    assert collection.LoadFiles(PATH1, PATH2) == 1
    tree = collection.GetTopicsTree()
    assert len(tree) == 424

def test_topics2():
    '''Verify the topics tree is returned regardless of load order.'''
    collection = sut.CHMCollection()
    assert collection.LoadFiles(PATH2, PATH1) == 1
    tree = collection.GetTopicsTree()
    assert len(tree) == 424

def test_index1():
    '''Verify the index is returned regardless of load order.'''
    collection = sut.CHMCollection()
    assert collection.LoadFiles(PATH1, PATH2) == 1
    index = collection.GetIndex()
    assert len(index) == 464

def test_index2():
    '''Verify the index is returned regardless of load order.'''
    collection = sut.CHMCollection()
    assert collection.LoadFiles(PATH2, PATH1) == 1
    index = collection.GetIndex()
    assert len(index) == 464

def test_encoding():
    '''Verify the encoding matches the component files' encoding.'''
    collection = sut.CHMCollection()
    assert collection.LoadFiles(PATH1, PATH2) == 1
    encoding = collection.files[0].encoding or collection.files[1].encoding
    assert collection.GetEncoding() == encoding

def test_lcid():
    '''Verify the LCID matches the component files' encoding.'''
    collection = sut.CHMCollection()
    assert collection.LoadFiles(PATH1, PATH2) == 1
    lcid = collection.files[0].GetLCID() or collection.files[1].GetLCID()
    assert collection.GetLCID() == lcid

def test_single1():
    '''Verify the TOC/Index aren't incorrectly reported for a single file.'''
    collection = sut.CHMCollection()
    assert collection.LoadFiles(PATH1) == 1
    assert collection.GetIndex() is not None
    assert collection.GetTopicsTree() is None

def test_single2():
    '''Verify the TOC/Index aren't incorrectly reported for a single file.'''
    collection = sut.CHMCollection()
    assert collection.LoadFiles(PATH2) == 1
    assert collection.GetIndex() is None
    assert collection.GetTopicsTree() is not None
