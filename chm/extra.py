# Copyright (C) 2019 Mikhail Gusarov <dottedmag@dottedmag.net>
#
# pychm is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; see the file COPYING.  If not,
# write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA

from . import chmlib, _chmlib

_lang_objects = [
    (b'/$FIftiMain', 0x7E),
    (b'$WWKeywordLinks/BTree', 0x34),
    (b'$WWAssociativeLinks/BTree', 0x34),
]

def get_lcid(f):
    for (obj, offset) in _lang_objects:
        (res, ui) = chmlib.chm_resolve_object(f, obj)
        if res == chmlib.CHM_RESOLVE_SUCCESS:
            (size, content) = chmlib.chm_retrieve_object(f, ui, offset, 4)
            if size != 0:
                return struct.unpack('<i', content)
    return None

def search(f, text, whole_words, titles_only):
    if not is_searchable(f):
        return False
    d = {}
    def cb(topic, url):
        d[topic] = url
    ret = _chmlib.search(f, text, whole_words, titles_only, cb)
    return ret, d

_search_objects = [b'/$FIftiMain', b'/#TOPICS', b'/#STRINGS', b'/#URLTBL',
                   b'/#URLSTR']

def is_searchable(chmfile):
    for obj in _search_objects:
        (res, _) = chmlib.chm_resolve_object(chmfile, obj)
        if res == chmlib.CHM_RESOLVE_FAILURE:
            return False
    return True
