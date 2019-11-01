from collections import namedtuple
from . import _chmlib
import sys

# Python 2 compatibility
try:
    unicode
except:
    unicode = str

CHM_UNCOMPRESSED = 0
CHM_COMPRESSED = 1

chmUnitInfo = namedtuple('chmUnitInfo',
                         ['start', 'length', 'space', 'flags', 'path'])

def chm_open(filename):
    if isinstance(filename, unicode):
        filename = filename.encode(sys.getfilesystemencoding())
    return _chmlib.chm_open(filename)

def chm_close(h):
    _chmlib.chm_close(h)

CHM_PARAM_MAX_BLOCKS_CACHED = 0

def chm_set_param(h, paramType, paramVal):
    _chmlib.chm_set_param(paramType, paramVal)

CHM_ENUMERATE_NORMAL = 1
CHM_ENUMERATE_META = 2
CHM_ENUMERATE_SPECIAL = 4
CHM_ENUMERATE_FILES = 8
CHM_ENUMERATE_DIRS = 16
CHM_ENUMERATE_ALL = 31

CHM_ENUMERATOR_FAILURE = 0
CHM_ENUMERATOR_CONTINUE = 1
CHM_ENUMERATOR_SUCCESS = 2

def chm_enumerate(h, what, e, context):
    def enumerator(ctx, ui, context):
        return e(ctx, chmUnitInfo._make(ui), context)
    return _chmlib.chm_enumerate(h, what, enumerator, context)

def chm_enumerate_dir(h, prefix, what, e, context):
    def enumerator(ctx, ui, context):
        return e(ctx, chmUnitInfo._make(ui), context)
    return _chmlib.chm_enumerate_dir(h, prefix, what, enumerator, context)

CHM_RESOLVE_SUCCESS = 0
CHM_RESOLVE_FAILURE = 1

def chm_resolve_object(h, path):
    out = _chmlib.chm_resolve_object(h, path)
    if out is not None:
        return CHM_RESOLVE_SUCCESS, chmUnitInfo._make(out)
    return CHM_RESOLVE_FAILURE, None

def chm_retrieve_object(h, ui, addr, length):
    buf = _chmlib.chm_retrieve_object(h, ui.start, ui.length, ui.space,
                                      addr, length)
    if buf is None:
        return 0, None
    return len(buf), buf
