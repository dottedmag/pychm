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

'''
extra
'''

from . import chmlib

def get_lcid(f):
    ret = chmlib.get_lcid(f)
    if ret == -1:
        return None
    return ret

def search(f, text, wholewords, titleonly):
    matches = {}
    partial = chmlib.search(f, text, wholewords, titleonly, matches)
    return (partial, matches)

def is_searchable(f):
    return chmlib.is_searchable(f)
