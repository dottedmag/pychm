# Copyright (C) 2003-2006 Rubens Ramos <rubensr@users.sourceforge.net>
#
# Based on code by:
# Copyright (C) 2003  Razvan Cojocaru <razvanco@gmx.net>
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
   chm - A high-level front end for the chmlib python module.

   The chm module provides high level access to the functionality
   included in chmlib. It encapsulates functions in the CHMFile class, and
   provides some additional features, such as the ability to obtain
   the contents tree of a CHM archive.

'''

from . import chmlib
from . import extra
import array
import posixpath
import sys

charset_table = {
    0: b'iso8859_1',  # ANSI_CHARSET
    238: b'iso8859_2',  # EASTEUROPE_CHARSET
    178: b'iso8859_6',  # ARABIC_CHARSET
    161: b'iso8859_7',  # GREEK_CHARSET
    177: b'iso8859_8',  # HEBREW_CHARSET
    162: b'iso8859_9',  # TURKISH_CHARSET
    222: b'iso8859_11',  # THAI_CHARSET
    186: b'iso8859_13',  # BALTIC_CHARSET
    204: b'cp1251',  # RUSSIAN_CHARSET
    255: b'cp437',  # OEM_CHARSET
    128: b'cp932',  # SHIFTJIS_CHARSET
    134: b'cp936',  # GB2312_CHARSET
    129: b'cp949',  # HANGUL_CHARSET
    136: b'cp950',  # CHINESEBIG5_CHARSET
    1: None,  # DEFAULT_CHARSET
    2: None,  # SYMBOL_CHARSET
    130: None,  # JOHAB_CHARSET
    163: None,  # VIETNAMESE_CHARSET
    77: None,  # MAC_CHARSET
}

locale_table = {
    0x0436: (b'iso8859_1', b'Afrikaans', b'Western Europe & US'),
    0x041c: (b'iso8859_2', b'Albanian', b'Central Europe'),
    0x0401: (b'iso8859_6', b'Arabic_Saudi_Arabia', b'Arabic'),
    0x0801: (b'iso8859_6', b'Arabic_Iraq', b'Arabic'),
    0x0c01: (b'iso8859_6', b'Arabic_Egypt', b'Arabic'),
    0x1001: (b'iso8859_6', b'Arabic_Libya', b'Arabic'),
    0x1401: (b'iso8859_6', b'Arabic_Algeria', b'Arabic'),
    0x1801: (b'iso8859_6', b'Arabic_Morocco', b'Arabic'),
    0x1c01: (b'iso8859_6', b'Arabic_Tunisia', b'Arabic'),
    0x2001: (b'iso8859_6', b'Arabic_Oman', b'Arabic'),
    0x2401: (b'iso8859_6', b'Arabic_Yemen', b'Arabic'),
    0x2801: (b'iso8859_6', b'Arabic_Syria', b'Arabic'),
    0x2c01: (b'iso8859_6', b'Arabic_Jordan', b'Arabic'),
    0x3001: (b'iso8859_6', b'Arabic_Lebanon', b'Arabic'),
    0x3401: (b'iso8859_6', b'Arabic_Kuwait', b'Arabic'),
    0x3801: (b'iso8859_6', b'Arabic_UAE', b'Arabic'),
    0x3c01: (b'iso8859_6', b'Arabic_Bahrain', b'Arabic'),
    0x4001: (b'iso8859_6', b'Arabic_Qatar', b'Arabic'),
    0x042b: (None, b'Armenian', b'Armenian'),
    0x042c: (b'iso8859_9', b'Azeri_Latin', b'Turkish'),
    0x082c: (b'cp1251', b'Azeri_Cyrillic', b'Cyrillic'),
    0x042d: (b'iso8859_1', b'Basque', b'Western Europe & US'),
    0x0423: (b'cp1251', b'Belarusian', b'Cyrillic'),
    0x0402: (b'cp1251', b'Bulgarian', b'Cyrillic'),
    0x0403: (b'iso8859_1', b'Catalan', b'Western Europe & US'),
    0x0404: (b'cp950', b'Chinese_Taiwan', b'Traditional Chinese'),
    0x0804: (b'cp936', b'Chinese_PRC', b'Simplified Chinese'),
    0x0c04: (b'cp950', b'Chinese_Hong_Kong', b'Traditional Chinese'),
    0x1004: (b'cp936', b'Chinese_Singapore', b'Simplified Chinese'),
    0x1404: (b'cp950', b'Chinese_Macau', b'Traditional Chinese'),
    0x041a: (b'iso8859_2', b'Croatian', b'Central Europe'),
    0x0405: (b'iso8859_2', b'Czech', b'Central Europe'),
    0x0406: (b'iso8859_1', b'Danish', b'Western Europe & US'),
    0x0413: (b'iso8859_1', b'Dutch_Standard', b'Western Europe & US'),
    0x0813: (b'iso8859_1', b'Dutch_Belgian', b'Western Europe & US'),
    0x0409: (b'iso8859_1', b'English_United_States', b'Western Europe & US'),
    0x0809: (b'iso8859_1', b'English_United_Kingdom', b'Western Europe & US'),
    0x0c09: (b'iso8859_1', b'English_Australian', b'Western Europe & US'),
    0x1009: (b'iso8859_1', b'English_Canadian', b'Western Europe & US'),
    0x1409: (b'iso8859_1', b'English_New_Zealand', b'Western Europe & US'),
    0x1809: (b'iso8859_1', b'English_Irish', b'Western Europe & US'),
    0x1c09: (b'iso8859_1', b'English_South_Africa', b'Western Europe & US'),
    0x2009: (b'iso8859_1', b'English_Jamaica', b'Western Europe & US'),
    0x2409: (b'iso8859_1', b'English_Caribbean', b'Western Europe & US'),
    0x2809: (b'iso8859_1', b'English_Belize', b'Western Europe & US'),
    0x2c09: (b'iso8859_1', b'English_Trinidad', b'Western Europe & US'),
    0x3009: (b'iso8859_1', b'English_Zimbabwe', b'Western Europe & US'),
    0x3409: (b'iso8859_1', b'English_Philippines', b'Western Europe & US'),
    0x0425: (b'iso8859_13', b'Estonian', b'Baltic'),
    0x0438: (b'iso8859_1', b'Faeroese', b'Western Europe & US'),
    0x0429: (b'iso8859_6', b'Farsi', b'Arabic'),
    0x040b: (b'iso8859_1', b'Finnish', b'Western Europe & US'),
    0x040c: (b'iso8859_1', b'French_Standard', b'Western Europe & US'),
    0x080c: (b'iso8859_1', b'French_Belgian', b'Western Europe & US'),
    0x0c0c: (b'iso8859_1', b'French_Canadian', b'Western Europe & US'),
    0x100c: (b'iso8859_1', b'French_Swiss', b'Western Europe & US'),
    0x140c: (b'iso8859_1', b'French_Luxembourg', b'Western Europe & US'),
    0x180c: (b'iso8859_1', b'French_Monaco', b'Western Europe & US'),
    0x0437: (None, b'Georgian', b'Georgian'),
    0x0407: (b'iso8859_1', b'German_Standard', b'Western Europe & US'),
    0x0807: (b'iso8859_1', b'German_Swiss', b'Western Europe & US'),
    0x0c07: (b'iso8859_1', b'German_Austrian', b'Western Europe & US'),
    0x1007: (b'iso8859_1', b'German_Luxembourg', b'Western Europe & US'),
    0x1407: (b'iso8859_1', b'German_Liechtenstein', b'Western Europe & US'),
    0x0408: (b'iso8859_7', b'Greek', b'Greek'),
    0x040d: (b'iso8859_8', b'Hebrew', b'Hebrew'),
    0x0439: (None, b'Hindi', b'Indic'),
    0x040e: (b'iso8859_2', b'Hungarian', b'Central Europe'),
    0x040f: (b'iso8859_1', b'Icelandic', b'Western Europe & US'),
    0x0421: (b'iso8859_1', b'Indonesian', b'Western Europe & US'),
    0x0410: (b'iso8859_1', b'Italian_Standard', b'Western Europe & US'),
    0x0810: (b'iso8859_1', b'Italian_Swiss', b'Western Europe & US'),
    0x0411: (b'cp932', b'Japanese', b'Japanese'),
    0x043f: (b'cp1251', b'Kazakh', b'Cyrillic'),
    0x0457: (None, b'Konkani', b'Indic'),
    0x0412: (b'cp949', b'Korean', b'Korean'),
    0x0426: (b'iso8859_13', b'Latvian', b'Baltic'),
    0x0427: (b'iso8859_13', b'Lithuanian', b'Baltic'),
    0x042f: (b'cp1251', b'Macedonian', b'Cyrillic'),
    0x043e: (b'iso8859_1', b'Malay_Malaysia', b'Western Europe & US'),
    0x083e: (b'iso8859_1', b'Malay_Brunei_Darussalam', b'Western Europe & US'),
    0x044e: (None, b'Marathi', b'Indic'),
    0x0414: (b'iso8859_1', b'Norwegian_Bokmal', b'Western Europe & US'),
    0x0814: (b'iso8859_1', b'Norwegian_Nynorsk', b'Western Europe & US'),
    0x0415: (b'iso8859_2', b'Polish', b'Central Europe'),
    0x0416: (b'iso8859_1', b'Portuguese_Brazilian', b'Western Europe & US'),
    0x0816: (b'iso8859_1', b'Portuguese_Standard', b'Western Europe & US'),
    0x0418: (b'iso8859_2', b'Romanian', b'Central Europe'),
    0x0419: (b'cp1251', b'Russian', b'Cyrillic'),
    0x044f: (None, b'Sanskrit', b'Indic'),
    0x081a: (b'iso8859_2', b'Serbian_Latin', b'Central Europe'),
    0x0c1a: (b'cp1251', b'Serbian_Cyrillic', b'Cyrillic'),
    0x041b: (b'iso8859_2', b'Slovak', b'Central Europe'),
    0x0424: (b'iso8859_2', b'Slovenian', b'Central Europe'),
    0x040a: (b'iso8859_1', b'Spanish_Trad_Sort', b'Western Europe & US'),
    0x080a: (b'iso8859_1', b'Spanish_Mexican', b'Western Europe & US'),
    0x0c0a: (b'iso8859_1', b'Spanish_Modern_Sort', b'Western Europe & US'),
    0x100a: (b'iso8859_1', b'Spanish_Guatemala', b'Western Europe & US'),
    0x140a: (b'iso8859_1', b'Spanish_Costa_Rica', b'Western Europe & US'),
    0x180a: (b'iso8859_1', b'Spanish_Panama', b'Western Europe & US'),
    0x1c0a: (b'iso8859_1', b'Spanish_Dominican_Repub', b'Western Europe & US'),
    0x200a: (b'iso8859_1', b'Spanish_Venezuela', b'Western Europe & US'),
    0x240a: (b'iso8859_1', b'Spanish_Colombia', b'Western Europe & US'),
    0x280a: (b'iso8859_1', b'Spanish_Peru', b'Western Europe & US'),
    0x2c0a: (b'iso8859_1', b'Spanish_Argentina', b'Western Europe & US'),
    0x300a: (b'iso8859_1', b'Spanish_Ecuador', b'Western Europe & US'),
    0x340a: (b'iso8859_1', b'Spanish_Chile', b'Western Europe & US'),
    0x380a: (b'iso8859_1', b'Spanish_Uruguay', b'Western Europe & US'),
    0x3c0a: (b'iso8859_1', b'Spanish_Paraguay', b'Western Europe & US'),
    0x400a: (b'iso8859_1', b'Spanish_Bolivia', b'Western Europe & US'),
    0x440a: (b'iso8859_1', b'Spanish_El_Salvador', b'Western Europe & US'),
    0x480a: (b'iso8859_1', b'Spanish_Honduras', b'Western Europe & US'),
    0x4c0a: (b'iso8859_1', b'Spanish_Nicaragua', b'Western Europe & US'),
    0x500a: (b'iso8859_1', b'Spanish_Puerto_Rico', b'Western Europe & US'),
    0x0441: (b'iso8859_1', b'Swahili', b'Western Europe & US'),
    0x041d: (b'iso8859_1', b'Swedish', b'Western Europe & US'),
    0x081d: (b'iso8859_1', b'Swedish_Finland', b'Western Europe & US'),
    0x0449: (None, b'Tamil', b'Indic'),
    0x0444: (b'cp1251', b'Tatar', b'Cyrillic'),
    0x041e: (b'iso8859_11', b'Thai', b'Thai'),
    0x041f: (b'iso8859_9', b'Turkish', b'Turkish'),
    0x0422: (b'cp1251', b'Ukrainian', b'Cyrillic'),
    0x0420: (b'iso8859_6', b'Urdu', b'Arabic'),
    0x0443: (b'iso8859_9', b'Uzbek_Latin', b'Turkish'),
    0x0843: (b'cp1251', b'Uzbek_Cyrillic', b'Cyrillic'),
    0x042a: (None, b'Vietnamese', b'Vietnamese')
}


class CHMFile:
    "A class to manage access to CHM files."
    filename = b''
    file = None
    title = b''
    home = b'/'
    index = None
    topics = None
    encoding = None
    lcid = None
    binaryindex = None

    def __init__(self):
        self.searchable = 0

    def LoadCHM(self, archiveName):
        '''Loads a CHM archive.
        This function will also call GetArchiveInfo to obtain information
        such as the index file name and the topics file. It returns 1 on
        success, and 0 if it fails.
        '''
        if self.filename != b'':
            self.CloseCHM()

        if isinstance(archiveName, str):
            archiveName = archiveName.encode(sys.getfilesystemencoding())

        self.file = chmlib.chm_open(archiveName)
        if self.file is None:
            return 0

        self.filename = archiveName
        self.GetArchiveInfo()

        return 1

    def CloseCHM(self):
        '''Closes the CHM archive.
        This function will close the CHM file, if it is open. All variables
        are also reset.
        '''
        if self.filename != b'':
            chmlib.chm_close(self.file)
            self.file = None
            self.filename = b''
            self.title = b''
            self.home = b'/'
            self.index = None
            self.topics = None
            self.encoding = None

    def GetArchiveInfo(self):
        '''Obtains information on CHM archive.
        This function checks the /#SYSTEM file inside the CHM archive to
        obtain the index, home page, topics, encoding and title. It is called
        from LoadCHM.
        '''

        self.searchable = extra.is_searchable(self.file)
        self.lcid = None

        result, ui = chmlib.chm_resolve_object(self.file, b'/#SYSTEM')
        if (result != chmlib.CHM_RESOLVE_SUCCESS):
            return 0

        size, text = chmlib.chm_retrieve_object(self.file, ui, 4, ui.length)
        if (size == 0):
            return 0

        buff = array.array('B', text)

        index = 0
        while (index < size):
            cursor = buff[index] + (buff[index+1] * 256)

            if (cursor == 0):
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
                self.topics = b'/' + text[index:index+cursor-1]
            elif (cursor == 1):
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
                self.index = b'/' + text[index:index+cursor-1]
            elif (cursor == 2):
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
                self.home = b'/' + text[index:index+cursor-1]
            elif (cursor == 3):
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
                self.title = text[index:index+cursor-1]
            elif (cursor == 4):
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
                self.lcid = buff[index] + (buff[index+1] * 256)
            elif (cursor == 6):
                index += 2
                cursor = buff[index] + (buff[index+1] * 256)
                index += 2
                tmp = text[index:index+cursor-1]
                if not self.topics:
                    tmp1 = b'/' + tmp + b'.hhc'
                    tmp2 = b'/' + tmp + b'.hhk'
                    res1, ui1 = chmlib.chm_resolve_object(self.file, tmp1)
                    res2, ui2 = chmlib.chm_resolve_object(self.file, tmp2)
                    if not self.topics and res1 == chmlib.CHM_RESOLVE_SUCCESS:
                        self.topics = b'/' + tmp + b'.hhc'
                    if not self.index and res2 == chmlib.CHM_RESOLVE_SUCCESS:
                        self.index = b'/' + tmp + b'.hhk'
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

        self.GetWindowsInfo()

        if not self.lcid:
            self.lcid = extra.get_lcid(self.file)

        return 1

    def GetTopicsTree(self):
        '''Reads and returns the topics tree.
        This auxiliary function reads and returns the topics tree file
        contents for the CHM archive.
        '''
        if self.topics is None:
            return None

        if self.topics:
            res, ui = chmlib.chm_resolve_object(self.file, self.topics)
            if (res != chmlib.CHM_RESOLVE_SUCCESS):
                return None

        size, text = chmlib.chm_retrieve_object(self.file, ui, 0, ui.length)
        if (size == 0):
            return None
        return text

    def GetIndex(self):
        '''Reads and returns the index tree.
        This auxiliary function reads and returns the index tree file
        contents for the CHM archive.
        '''
        if self.index is None:
            return None

        if self.index:
            res, ui = chmlib.chm_resolve_object(self.file, self.index)
            if (res != chmlib.CHM_RESOLVE_SUCCESS):
                return None

        size, text = chmlib.chm_retrieve_object(self.file, ui, 0, ui.length)
        if (size == 0):
            return None
        return text

    def ResolveObject(self, document):
        '''Tries to locate a document in the archive.
        This function tries to locate the document inside the archive. It
        returns a tuple where the first element is zero if the function
        was successful, and the second is the UnitInfo for that document.
        The UnitInfo is used to retrieve the document contents
        '''
        if self.file:
            path = posixpath.normpath(document)
            return chmlib.chm_resolve_object(self.file, path)
        else:
            return (1, None)

    def RetrieveObject(self, ui, start=-1, length=-1):
        '''Retrieves the contents of a document.
        This function takes a UnitInfo and two optional arguments, the first
        being the start address and the second is the length. These define
        the amount of data to be read from the archive.
        '''
        if self.file and ui:
            if start == -1:
                offset = 0
            else:
                offset = start
            if length == -1:
                size = ui.length - offset
            else:
                size = length

            content = b''
            while size > 0:
                (sz, chunk) = chmlib.chm_retrieve_object(self.file, ui, offset, size)
                if sz == 0:
                    return (0, b'')
                content += chunk[:sz]
                size -= sz
                offset += sz

            return (len(content), content)
        else:
            return (0, b'')

    def Search(self, text, wholewords=0, titleonly=0):
        '''Performs full-text search on the archive.
        The first parameter is the word to look for, the second
        indicates if the search should be for whole words only, and
        the third parameter indicates if the search should be
        restricted to page titles.
        This method will return a tuple, the first item
        indicating if the search results were partial, and the second
        item being a dictionary containing the results.'''
        if text and text != b'' and self.file:
            return extra.search(self.file, text, wholewords,
                                titleonly)
        else:
            return None

    def IsSearchable(self):
        '''Indicates if the full-text search is available for this
        archive - this flag is updated when GetArchiveInfo is called'''
        return self.searchable

    def GetEncoding(self):
        '''Returns a string that can be used with the codecs python package
        to encode or decode the files in the chm archive. If an error is
        found, or if it is not possible to find the encoding, None is
        returned.'''
        if self.encoding:
            vals = self.encoding.split(b',')
            if len(vals) > 2:
                try:
                    return charset_table[int(vals[2])]
                except KeyError:
                    pass
        return None

    def GetLCID(self):
        '''Returns the archive Locale ID'''
        if self.lcid in locale_table:
            return locale_table[self.lcid]
        else:
            return None

    def GetDWORD(self, buff, idx=0):
        '''Internal method.
        Reads a double word (4 bytes) from a buffer.
        '''
        result = buff[idx] + (buff[idx+1] << 8) + (buff[idx+2] << 16) + \
            (buff[idx+3] << 24)

        if result == 0xFFFFFFFF:
            result = 0

        return result

    def GetString(self, text, idx):
        '''Internal method.
        Retrieves a string from the #STRINGS buffer.
        '''
        next = text.find(b'\x00', idx)
        chunk = text[idx:next]
        return chunk

    def GetWindowsInfo(self):
        '''Gets information from the #WINDOWS file.
        Checks the #WINDOWS file to see if it has any info that was
        not found in #SYSTEM (topics, index or default page.
        '''
        result, ui = chmlib.chm_resolve_object(self.file, b'/#WINDOWS')
        if (result != chmlib.CHM_RESOLVE_SUCCESS):
            return -1

        size, text = chmlib.chm_retrieve_object(self.file, ui, 0, 8)
        if (size < 8):
            return -2

        buff = array.array('B', text)
        num_entries = self.GetDWORD(buff, 0)
        entry_size = self.GetDWORD(buff, 4)

        if num_entries < 1:
            return -3

        size, text = chmlib.chm_retrieve_object(self.file, ui, 8, entry_size)
        if (size < entry_size):
            return -4

        buff = array.array('B', text)
        toc_index = self.GetDWORD(buff, 0x60)
        idx_index = self.GetDWORD(buff, 0x64)
        dft_index = self.GetDWORD(buff, 0x68)

        result, ui = chmlib.chm_resolve_object(self.file, b'/#STRINGS')
        if (result != chmlib.CHM_RESOLVE_SUCCESS):
            return -5

        size, text = chmlib.chm_retrieve_object(self.file, ui, 0, ui.length)
        if (size == 0):
            return -6

        if (not self.topics):
            self.topics = self.GetString(text, toc_index)
            if not self.topics.startswith(b'/'):
                self.topics = b'/' + self.topics

        if (not self.index):
            self.index = self.GetString(text, idx_index)
            if not self.index.startswith(b'/'):
                self.index = b'/' + self.index

        if (dft_index != 0):
            self.home = self.GetString(text, dft_index)
            if not self.home.startswith(b'/'):
                self.home = b'/' + self.home
