## Copyright (C) 2003 Rubens Ramos <rubensr@users.sourceforge.net>

## Based on code by:
## Copyright (C) 2003  Razvan Cojocaru <razvanco@gmx.net>

## pychm is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.

## You should have received a copy of the GNU General Public
## License along with this program; see the file COPYING.  If not,
## write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
## Boston, MA 02111-1307, USA

## $Id$

'''
   chm - A high-level front end for the chmlib python module.

   The chm module provides high level access to the functionality
   included in chmlib. It encapsulates functions in the CHMFile class, and
   provides some additional features, such as the ability to obtain
   the contents tree of a CHM file.
   
'''

import chmlib
import array
import string
import os.path
import re
from HTMLParser import HTMLParser

def print_index_tree(node, pre = ''):
    if node == None:
        return
    if node.get_data() != None:
        print pre + str(node.get_data())
    print_index_tree(node.get_child(), pre + '  ')
    print_index_tree(node.get_next(), pre)

def get_index_path(node, path):
    if node == None:
        result = path
    else:
        aux = node.get_prev()
        idx = 0
        while aux != None:
            idx += 1
            aux = aux.get_prev()
        npath = get_index_path(node.get_parent(), path)
        npath.append(idx)
        result = npath
    return result

def get_index_node_on_path(node, path):
    if node == None:
        return None
    car = path[0]
    cdr = path[1:]
    aux = node
    idx = 0
    while idx < car:
        aux = aux.get_next()
        idx += 1
    if cdr == []:
        result = aux
    else:
        result = get_index_node_on_path(aux.get_child(), cdr)
    return result

class IndexNode:
    parent  = None
    next = None
    child = None
    data = None
    prev = None
    
    def __init__(self, data):
        self.data = data
        
    def set_parent(self, node):
        self.parent = node

    def set_next(self, next):
        self.next = next

    def set_prev(self, prev):
        self.prev = prev

    def set_child(self, child):
        self.child = child

    def get_parent(self):
        return self.parent

    def get_next(self):
        return self.next

    def get_prev(self):
        return self.prev

    def get_child(self):
        return self.child

    def get_data(self):
        return self.data

    def get_n_children(self):
        num = 0;
        aux = self.get_child()
        while aux != None:
            num += 1
            aux = aux.get_next()
        return num

    def get_n_child(self, idx):
        num = 0;
        aux = self.get_child()
        while aux != None and num < idx:
            num += 1
            aux = aux.get_next()
        return aux

    def kill(self):
        if self.child:
            self.child.kill()
            self.child = None
        if self.next:
            self.next.kill()
            self.next = None
        self.data = None

class IndexParser(HTMLParser):
    "A parser for a Topics file"
    in_obj = 0
    name = ""
    local = ""
    param = ""
    add_level = 0
    
    def __init__(self):
        HTMLParser.__init__(self)
        self.root = None
        self.current = self.root
        
    def handle_starttag(self, tag, attrs):
        if (tag == "ul"):
            self.add_level = 1
        elif (tag == "object"):
            for x, y in attrs:
                if ((x.lower() == "type") and (y.lower() == "text/sitemap")):
                    self.in_obj = 1
        elif ((tag.lower() == "param") and (self.in_obj == 1)):
            for x, y in attrs:
                if (x.lower() == "name"):
                    self.param = y.lower()
                elif (x.lower() == "value"):
                    if (self.param.lower() == "name") and (self.name == ""):
                        self.name = y.lower()
                    elif (self.param.lower() == "local"):
                        self.local = y.lower()
                    elif (self.param.lower() == "merge"):
                        self.in_obj = 0

    def handle_endtag(self, tag):
        if (tag == "ul") and self.current:
            self.current = self.current.get_parent()
        elif (tag == "object") and (self.in_obj == 1):
            val = (self.name, self.local)
            node = IndexNode(val)
            if self.add_level == 1:
                if self.root == None:
                    self.root = node
                else:
                    node.set_parent(self.current)
                    if not self.current:
                        self.root.set_next(node)
                        node.set_prev(self.root)
                    else:
                        self.current.set_child(node)
                self.add_level = 0
            else:
                if self.current:
                    node.set_parent(self.current.get_parent())
                    self.current.set_next(node)
                    node.set_prev(self.current)
                else:
                    node.set_prev(self.root)
                    self.root.set_next(node)
            self.current = node
            self.in_obj = 0
            self.name = ""
            self.local = ""
        
class CHMFile:
    "A class to manage access to CHM files."
    filename = ""
    file = None
    title = ""
    home = "/"
    index = None
    topics = None
    encoding = None
    
    def __init__(self):
        pass
    
    def LoadCHM(self, archiveName):
        if (self.filename != None):
            self.CloseCHM()

        self.file = chmlib.chm_open(archiveName)
        if (self.file == None):
            return 0

        self.filename = archiveName
        self.GetArchiveInfo()

        return 1

    def CloseCHM(self):
        if (self.filename != None):
            chmlib.chm_close(self.file)

    def GetArchiveInfo(self):
        result, ui = chmlib.chm_resolve_object(self.file, '/#SYSTEM')
        if (result != chmlib.CHM_RESOLVE_SUCCESS):
            print 'GetArchiveInfo: #SYSTEM does not exist'
            return 0
        
        size, text = chmlib.chm_retrieve_object(self.file, ui, 4l, ui.length)
        if (size == 0):
            print 'GetArchiveInfo: file size = 0'
            return 0

        buff = array.array('B', text)

        index = 0
        while (index < size):
            cursor = buff[index] + (buff[index+1] * 256)

            if (cursor == 0):
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
                self.topics = '/' + text[index:index+cursor-1]
            elif (cursor == 1):
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
                self.index = '/' + text[index:index+cursor-1]
            elif (cursor == 2):
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
                self.home = '/' + text[index:index+cursor-1]
            elif (cursor == 3):
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
                self.title = text[index:index+cursor-1]
            elif (cursor == 6):
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
                tmp = text[index:index+cursor-1]
                if not self.topics:
                    tmp1 = '/' + tmp + '.hhc'
                    tmp2 = '/' + tmp + '.hhk'
                    res1, ui1 = chmlib.chm_resolve_object(self.file, tmp1)
                    res2, ui2 = chmlib.chm_resolve_object(self.file, tmp2)
                    if (res1 == chmlib.CHM_RESOLVE_SUCCESS):
                        self.topics = '/' + tmp + '.hhc'
                    elif (res2 == chmlib.CHM_RESOLVE_SUCCESS):
                        self.index = '/' + tmp + '.hhk'
            elif (cursor == 16):
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
                self.encoding = text[index:index+cursor-1]
            else:
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
            index += cursor
        if ((not self.topics) and (not self.index)):
            result, ui = chmlib.chm_resolve_object(self.file, '/#STRINGS')
            if (result != chmlib.CHM_RESOLVE_SUCCESS):
                print 'GetArchiveInfo: Could not find #STRINGS'
                return 1
            
            size, text = chmlib.chm_retrieve_object(self.file, ui, 1l,
                                                    ui.length)
            if (size == 0):
                print 'GetArchiveInfo: STRINGS file size = 0'
                return 1

            index = 0
            while (index < size):
                next = string.find(text, '\x00', index)
                chunk = text[index:next]
                ext = string.lower(chunk[-4:])
                if (ext == '.hhc'):
                    self.topics = '/' + chunk
                elif (ext == '.hhk'):
                   self.index = '/' + chunk
                index = next + 1
        return 1

    def GetTopicsTree(self):
        if (self.topics == None):
            return None

        if self.topics:
            res, ui = chmlib.chm_resolve_object(self.file, self.topics)
            if (res != chmlib.CHM_RESOLVE_SUCCESS):
                return None

        size, text = chmlib.chm_retrieve_object(self.file, ui, 0l, ui.length)
        if (size == 0):
            print 'GetTopicsTree: file size = 0'
            return None

        parser = IndexParser()
        parser.feed(text)
        return parser.root

    def GetIndex(self):
        if (self.index == None):
            return None

        if self.index:
            res, ui = chmlib.chm_resolve_object(self.file, self.index)
            if (res != chmlib.CHM_RESOLVE_SUCCESS):
                return None

        size, text = chmlib.chm_retrieve_object(self.file, ui, 0l, ui.length)
        if (size == 0):
            print 'GetIndex: file size = 0'
            return None

        parser = IndexParser()
        parser.feed(text)
        return parser.root

    def ResolveObject(self, document):
        if self.file:
            path = os.path.abspath(document)
            return chmlib.chm_resolve_object(self.file, path)
        else:
            return (1, None)

    def RetrieveObject(self, ui, start = -1, length = -1):
        if self.file and ui:
            if length == -1:
                len = ui.length
            if start == -1:
                st = 0l
            return chmlib.chm_retrieve_object(self.file, ui, st, len)
        else:
            return (0, '')

    def IndexSearch(self, pattern, wholewords, titleonly):
        if (not pattern) or pattern == '':
            return None
        r, ui = chmlib.chm_resolve_object(self.file, '/$FIftiMain')
        if r:
            return None
        r, uitopics = chmlib.chm_resolve_object(self.file, '/#TOPICS')
        if r:
            return None
        r, uistrings = chmlib.chm_resolve_object(self.file, '/#STRINGS')
        if r:
            return None
        r, uiurltbl = chmlib.chm_resolve_object(self.file, '/#URLTBL')
        if r:
            return None
        r, uiurlstr = chmlib.chm_resolve_object(self.file, '/#URLSTR')
        if r:
            return None
        regexp = re.compile(pattern)
        size, header = chmlib.chm_retrieve_object(self.file, ui, ol, 0x32)
        if size == 0:
            return None
        return None
