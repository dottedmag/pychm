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
   the contents tree of a CHM archive.
   
'''

import chmlib
import array
import string
import os.path
import re

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
        '''Loads a CHM archive.
        This function will also call GetArchiveInfo to obtain information
        such as the index file name and the topics file. It returns 1 on
        success, and 0 if it fails.
        '''
        if (self.filename != None):
            self.CloseCHM()

        self.file = chmlib.chm_open(archiveName)
        if (self.file == None):
            return 0

        self.filename = archiveName
        self.GetArchiveInfo()

        return 1

    def CloseCHM(self):
        '''Closes the CHM archive
        This function will close the CHM file, if it is open. All variables
        are also reset.
        '''
        if (self.filename != None):
            chmlib.chm_close(self.file)
            self.file = None
            self.filename = ''
            self.title = ""
            self.home = "/"
            self.index = None
            self.topics = None
            self.encoding = None

    def GetArchiveInfo(self):
        '''Obtains information on CHM archive.
        This function checks the /#SYSTEM file inside the CHM archive to
        obtain the index, home page, topics, encoding and title
        '''
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
        '''Reads and returns the topics tree
        This auxiliary function reads and returns the topics tree file
        contents for the CHM archive.
        '''
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
        return text

    def GetIndex(self):
        '''Reads and returns the index tree
        This auxiliary function reads and returns the index tree file
        contents for the CHM archive.
        '''
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
        return text

    def ResolveObject(self, document):
        '''Tries to locate a document in the archive
        This function tries to locate the document inside the archive. It
        returns a tuple where the first element is zero if the function
        was successful, and the second is the UnitInfo for that document.
        The UnitInfo is used to retrieve the document contents
        '''
        if self.file:
            path = os.path.abspath(document)
            return chmlib.chm_resolve_object(self.file, path)
        else:
            return (1, None)

    def RetrieveObject(self, ui, start = -1, length = -1):
        '''Retrieves the contents of a document
        This function takes a UnitInfo and two optional arguments, the first
        being the start address and the second is the length. These define
        the amount of data to be read from the archive.
        '''
        if self.file and ui:
            if length == -1:
                len = ui.length
            if start == -1:
                st = 0l
            return chmlib.chm_retrieve_object(self.file, ui, st, len)
        else:
            return (0, '')

    def IndexSearch(self, pattern, wholewords, titleonly):
        '''This is not working yet!'''
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
