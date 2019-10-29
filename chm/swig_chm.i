%module chmlib
%begin %{
#define SWIG_PYTHON_STRICT_BYTE_CHAR
%}

%include "typemaps.i"
%include "cstring.i"

%{
/*
 Copyright (C) 2003 Rubens Ramos <rubensr@users.sourceforge.net>
 Copyright (C) 2019 Mikhail Gusarov <dottedmag@dottedmag.net>

 Based on code by:
 Copyright (C) 2003  Razvan Cojocaru <razvanco@gmx.net>

 pychm is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License as
 published by the Free Software Foundation; either version 2 of the
 License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU General Public
 License along with this program; see the file COPYING.  If not,
 write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 Boston, MA 02111-1307, USA

 $Id$
*/
#include "chm_lib.h"
#include <stdio.h>

static PyObject *my_callback = NULL;

static PyObject *
my_set_callback(PyObject *dummy, PyObject *arg)
{
    PyObject *result = NULL;

    if (!PyCallable_Check(arg)) {
      PyErr_SetString(PyExc_TypeError, "parameter must be callable");
      return NULL;
    }
    Py_XINCREF(arg);         /* Add a reference to new callback */
    Py_XDECREF(my_callback);  /* Dispose of previous callback */
    my_callback = arg;       /* Remember new callback */
    /* Boilerplate to return "None" */
    Py_INCREF(Py_None);
    result = Py_None;
    return result;
}

int dummy_enumerator (struct chmFile *h,
                      struct chmUnitInfo *ui,
                      void *context) {
    PyObject *arglist;
    PyObject *result;
    PyObject *py_h;
    PyObject *py_ui;
    PyObject *py_c;

    py_h  = SWIG_NewPointerObj((void *) h, SWIGTYPE_p_chmFile, 0);
    py_ui = SWIG_NewPointerObj((void *) ui, SWIGTYPE_p_chmUnitInfo, 0);
    py_c  = PyCapsule_New(context, "context", NULL);

    /* Time to call the callback */
    arglist = Py_BuildValue("(OOO)", py_h, py_ui, py_c);
    if (arglist) {
      result = PyEval_CallObject(my_callback, arglist);
      Py_DECREF(arglist);

      Py_DECREF(py_h);
      Py_DECREF(py_ui);
      Py_DECREF(py_c);

      if (result == NULL) {
        return 0; /* Pass error back */
      } else {
        Py_DECREF(result);
        return 1;
      }
    } else {
      return 0;
    }
 }

#define false 0
#define true 1

#define FTS_HEADER_LEN 0x32
#define TOPICS_ENTRY_LEN 16
#define COMMON_BUF_LEN 1025

#define FREE(x) free (x); x = NULL

static uint16_t
get_uint16 (uint8_t* b) {
  return b[0] |
    b[1]<<8;
}

static uint32_t
get_uint32 (uint8_t* b) {
  return b[0] |
    b[1]<<8   |
    b[2]<<16  |
    b[3]<<24;
}

static uint64_t
be_encint (unsigned char *buffer, size_t *length)
{
  uint64_t result = 0;
  int shift=0;
  *length = 0;

  do {
    result |= ((*buffer) & 0x7f) << shift;
    shift += 7;
    *length = *length + 1;

  } while (*(buffer++) & 0x80);

  return result;
}

/*
  Finds the first unset bit in memory. Returns the number of set bits found.
  Returns -1 if the buffer runs out before we find an unset bit.
*/
static int
ffus (unsigned char* byte, int* bit, size_t *length) {
  int bits = 0;
  *length = 0;

  while(*byte & (1 << *bit)){
    if(*bit)
      --(*bit);
    else {
      ++byte;
      ++(*length);
      *bit = 7;
    }
    ++bits;
  }

  if(*bit)
    --(*bit);
  else {
    ++(*length);
    *bit = 7;
  }

  return bits;
}


static uint64_t
sr_int(unsigned char* byte, int* bit,
       unsigned char s, unsigned char r, size_t *length)
{
  uint64_t ret;
  unsigned char mask;
  int n, n_bits, num_bits, base, count;
  size_t fflen;

  *length = 0;

  if(!bit || *bit > 7 || s != 2)
    return ~(uint64_t)0;
  ret = 0;

  count = ffus(byte, bit, &fflen);
  *length += fflen;
  byte += *length;

  n_bits = n = r + (count ? count-1 : 0) ;

  while (n > 0) {
    num_bits = n > *bit ? *bit : n-1;
    base = n > *bit ? 0 : *bit - (n-1);

    switch (num_bits){
    case 0:
      mask = 1;
      break;
    case 1:
      mask = 3;
      break;
    case 2:
      mask = 7;
      break;
    case 3:
      mask = 0xf;
      break;
    case 4:
      mask = 0x1f;
      break;
    case 5:
      mask = 0x3f;
      break;
    case 6:
      mask = 0x7f;
      break;
    case 7:
      mask = 0xff;
      break;
    default:
      mask = 0xff;
      break;
    }

    mask <<= base;
    ret = (ret << (num_bits+1)) |
      (uint64_t)((*byte & mask) >> base);

    if( n > *bit ){
      ++byte;
      ++(*length);
      n -= *bit+1;
      *bit = 7;
    } else {
      *bit -= n;
      n = 0;
    }
  }

  if(count)
    ret |= (uint64_t)1 << n_bits;

  return ret;
}


static uint32_t
get_leaf_node_offset(struct chmFile *chmfile,
                     const char *text,
                     uint32_t initial_offset,
                     uint32_t buff_size,
                     uint16_t tree_depth,
                     struct chmUnitInfo *ui)
{
  unsigned char word_len;
  unsigned char pos;
  uint16_t free_space;
  char *wrd_buf;
  char *word = NULL;
  uint32_t test_offset = 0;
  uint32_t i = sizeof(uint16_t);
  unsigned char *buffer = malloc (buff_size);

  if (NULL == buffer)
    return 0;

  while (--tree_depth) {
    if (initial_offset == test_offset) {
      FREE(buffer);
      return 0;
    }

    test_offset = initial_offset;
    if (chm_retrieve_object (chmfile, ui, buffer,
                             initial_offset, buff_size) == 0) {
      FREE(buffer);
      return 0;
    }

    free_space = get_uint16 (buffer);

    while (i < buff_size - free_space) {

      word_len = *(buffer + i);
      pos = *(buffer + i + 1);

      wrd_buf = malloc (word_len);
      memcpy (wrd_buf, buffer + i + 2, word_len - 1);
      wrd_buf[word_len - 1] = 0;

      if (pos == 0) {
        FREE (word);
        word = (char *) strdup (wrd_buf);
      } else {
        word = realloc (word, word_len + pos + 1);
        strcpy (word + pos, wrd_buf);
      }

      FREE(wrd_buf);

      if (strcasecmp (text, word) <= 0) {
        initial_offset = get_uint32 (buffer + i + word_len + 1);
        break;
      }

      i += word_len + sizeof (unsigned char) + sizeof(uint32_t) +
        sizeof(uint16_t);
    }
  }

  if(initial_offset == test_offset)
    initial_offset = 0;

  FREE(word);
  FREE(buffer);

  return initial_offset;
}

static int
pychm_process_wlc (struct chmFile *chmfile,
                   uint64_t wlc_count, uint64_t wlc_size,
                   uint32_t wlc_offset, unsigned char ds,
                   unsigned char dr, unsigned char cs,
                   unsigned char cr, unsigned char ls,
                   unsigned char lr, struct chmUnitInfo *uimain,
                   struct chmUnitInfo* uitbl,
                   struct chmUnitInfo *uistrings,
                   struct chmUnitInfo* topics,
                   struct chmUnitInfo *urlstr,
                   PyObject *dict)
{
  uint32_t stroff, urloff;
  uint64_t i, j, count;
  size_t length;
  int wlc_bit = 7;
  size_t off = 0;
  uint64_t index = 0;
  unsigned char entry[TOPICS_ENTRY_LEN];
  unsigned char combuf[COMMON_BUF_LEN];
  unsigned char *buffer = malloc (wlc_size);
  char *url = NULL;
  char *topic = NULL;

  if (chm_retrieve_object(chmfile, uimain, buffer,
                          wlc_offset, wlc_size) == 0) {
    FREE(buffer);
    return false;
  }

  for (i = 0; i < wlc_count; ++i) {

    if(wlc_bit != 7) {
      ++off;
      wlc_bit = 7;
    }

    index += sr_int(buffer + off, &wlc_bit, ds, dr, &length);
    off += length;

    if(chm_retrieve_object(chmfile, topics, entry,
                           index * 16, TOPICS_ENTRY_LEN) == 0) {
      FREE(topic);
      FREE(url);
      FREE(buffer);
      return false;
    }

    combuf[COMMON_BUF_LEN - 1] = 0;
    stroff = get_uint32 (entry + 4);

    FREE (topic);
    if (chm_retrieve_object (chmfile, uistrings, combuf,
                             stroff, COMMON_BUF_LEN - 1) == 0) {
      topic = strdup ("Untitled in index");

    } else {
      combuf[COMMON_BUF_LEN - 1] = 0;

      topic = strdup ((char *)combuf);
    }

    urloff = get_uint32 (entry + 8);

    if(chm_retrieve_object (chmfile, uitbl, combuf,
                            urloff, 12) == 0) {
      FREE(buffer);
      return false;
    }

    urloff = get_uint32 (combuf + 8);

    if (chm_retrieve_object (chmfile, urlstr, combuf,
                             urloff + 8, COMMON_BUF_LEN - 1) == 0) {
      FREE(topic);
      FREE(url);
      FREE(buffer);
      return false;
    }

    combuf[COMMON_BUF_LEN - 1] = 0;

    FREE (url);
    url = strdup ((char *)combuf);

    if (url && topic) {
      PyDict_SetItemString (dict, topic,
                            PyString_FromString (url));
    }

    count = sr_int (buffer + off, &wlc_bit, cs, cr, &length);
    off += length;

    for (j = 0; j < count; ++j) {
      sr_int (buffer + off, &wlc_bit, ls, lr, &length);
      off += length;
    }
  }

  FREE(topic);
  FREE(url);
  FREE(buffer);

  return true;
}

typedef struct {
  const char *file;
  int offset;
} Langrec;

static Langrec lang_files[] = {
  {"/$FIftiMain",               0x7E},
  {"$WWKeywordLinks/BTree",     0x34},
  {"$WWAssociativeLinks/BTree", 0x34}
};

#define LANG_FILES_SIZE (sizeof(lang_files)/sizeof(Langrec))

%}

%inline %{

static int
search (struct chmFile *chmfile,
            const char *text, int whole_words,
            int titles_only, PyObject *dict)
{
  unsigned char header[FTS_HEADER_LEN];
  unsigned char doc_index_s;
  unsigned char doc_index_r;
  unsigned char code_count_s;
  unsigned char code_count_r;
  unsigned char loc_codes_s;
  unsigned char loc_codes_r;
  unsigned char word_len, pos;
  unsigned char *buffer;
  char *word = NULL;
  uint32_t node_offset;
  uint32_t node_len;
  uint16_t tree_depth;
  uint32_t i;
  uint16_t free_space;
  uint64_t wlc_count, wlc_size;
  uint32_t wlc_offset;
  char *wrd_buf;
  unsigned char title;
  size_t encsz;
  struct chmUnitInfo ui, uitopics, uiurltbl, uistrings, uiurlstr;
  int partial = false;

  if (NULL == text)
    return -1;

  if (chm_resolve_object (chmfile, "/$FIftiMain", &ui) !=
      CHM_RESOLVE_SUCCESS ||
      chm_resolve_object (chmfile, "/#TOPICS", &uitopics) !=
      CHM_RESOLVE_SUCCESS ||
      chm_resolve_object (chmfile, "/#STRINGS", &uistrings) !=
      CHM_RESOLVE_SUCCESS ||
      chm_resolve_object (chmfile, "/#URLTBL", &uiurltbl) !=
      CHM_RESOLVE_SUCCESS ||
      chm_resolve_object (chmfile, "/#URLSTR", &uiurlstr) !=
      CHM_RESOLVE_SUCCESS)
    return false;

  if(chm_retrieve_object(chmfile, &ui, header, 0, FTS_HEADER_LEN) == 0)
    return false;

  doc_index_s = header[0x1E];
  doc_index_r = header[0x1F];
  code_count_s = header[0x20];
  code_count_r = header[0x21];
  loc_codes_s = header[0x22];
  loc_codes_r = header[0x23];

  if(doc_index_s != 2 || code_count_s != 2 || loc_codes_s != 2) {
    return false;
  }

  node_offset = get_uint32 (header + 0x14);
  node_len = get_uint32 (header + 0x2e);
  tree_depth = get_uint16 (header + 0x18);

  i = sizeof(uint16_t);

  buffer = malloc (node_len);

  node_offset = get_leaf_node_offset (chmfile, text, node_offset, node_len,
                                      tree_depth, &ui);

  if (!node_offset) {
    FREE(buffer);
    return false;
  }

  do {

    if (chm_retrieve_object (chmfile, &ui, buffer,
                             node_offset, node_len) == 0) {
      FREE(word);
      FREE(buffer);
      return false;
    }

    free_space = get_uint16 (buffer + 6);

    i = sizeof(uint32_t) + sizeof(uint16_t) + sizeof(uint16_t);

    encsz = 0;

    while (i < node_len - free_space) {
      word_len = *(buffer + i);
      pos = *(buffer + i + 1);

      wrd_buf = malloc (word_len);
      memcpy (wrd_buf, buffer + i + 2, word_len - 1);
      wrd_buf[word_len - 1] = 0;

      if (pos == 0) {
        FREE(word);
        word = (char *) strdup (wrd_buf);
      } else {
        word = realloc (word, word_len + pos + 1);
        strcpy (word + pos, wrd_buf);
      }

      FREE(wrd_buf);

      i += 2 + word_len;
      title = *(buffer + i - 1);

      wlc_count = be_encint (buffer + i, &encsz);
      i += encsz;

      wlc_offset = get_uint32 (buffer + i);

      i += sizeof(uint32_t) + sizeof(uint16_t);
      wlc_size =  be_encint (buffer + i, &encsz);
      i += encsz;

      node_offset = get_uint32 (buffer);

      if (!title && titles_only)
        continue;

      if (whole_words && !strcasecmp(text, word)) {
        partial = pychm_process_wlc (chmfile, wlc_count, wlc_size,
                                     wlc_offset, doc_index_s,
                                     doc_index_r,code_count_s,
                                     code_count_r, loc_codes_s,
                                     loc_codes_r, &ui, &uiurltbl,
                                     &uistrings, &uitopics,
                                     &uiurlstr, dict);
        FREE(word);
        FREE(buffer);
        return partial;
      }

      if (!whole_words) {
        if (!strncasecmp (word, text, strlen(text))) {
          partial = true;
          pychm_process_wlc (chmfile, wlc_count, wlc_size,
                             wlc_offset, doc_index_s,
                             doc_index_r,code_count_s,
                             code_count_r, loc_codes_s,
                             loc_codes_r, &ui, &uiurltbl,
                             &uistrings, &uitopics,
                             &uiurlstr, dict);

        } else if (strncasecmp (text, word, strlen(text)) < -1)
          break;
      }

    }
  } while (!whole_words &&
           !strncmp (word, text, strlen(text)) &&
           node_offset);

  FREE(word);
  FREE(buffer);

  return partial;
}

static int
is_searchable (struct chmFile *file) {
  struct chmUnitInfo ui;

    if (chm_resolve_object (file, "/$FIftiMain", &ui) !=
        CHM_RESOLVE_SUCCESS ||
        chm_resolve_object (file, "/#TOPICS", &ui) !=
        CHM_RESOLVE_SUCCESS ||
        chm_resolve_object (file, "/#STRINGS", &ui) !=
        CHM_RESOLVE_SUCCESS ||
        chm_resolve_object (file, "/#URLTBL", &ui) !=
        CHM_RESOLVE_SUCCESS ||
        chm_resolve_object (file, "/#URLSTR", &ui) !=
        CHM_RESOLVE_SUCCESS)
        return false;
    else
        return true;
}

static int
get_lcid (struct chmFile *chmfile) {
  struct chmUnitInfo ui;
  uint32_t lang;
  int i;

  for (i=0; i<LANG_FILES_SIZE; i++) {

    if (chm_resolve_object (chmfile, lang_files[i].file, &ui) ==
        CHM_RESOLVE_SUCCESS) {

      if (chm_retrieve_object (chmfile, &ui, (unsigned char *) &lang,
                               lang_files[i].offset, sizeof(uint32_t)) != 0)
        return lang;
    }
  }

  return -1;
}

%}

%typemap(in) CHM_ENUMERATOR {
  if (!my_set_callback(self, $input)) goto fail;
  $1 = dummy_enumerator;
}

%typemap(in) void *context {
  if (!($1 = PyCapsule_New($input, "context", NULL))) goto fail;
}

%typemap(in, numinputs=0) struct chmUnitInfo *OutValue (struct chmUnitInfo *temp = (struct chmUnitInfo *) calloc(1, sizeof(struct chmUnitInfo))) {
  $1 = temp;
}

%typemap(argout) struct chmUnitInfo *OutValue {
  PyObject *o, *o2, *o3;
  o = SWIG_NewPointerObj((void *) $1, SWIGTYPE_p_chmUnitInfo, 1);
  if ((!$result) || ($result == Py_None)) {
    $result = o;
  } else {
    if (!PyTuple_Check($result)) {
      PyObject *o2 = $result;
      $result = PyTuple_New(1);
      PyTuple_SetItem($result,0,o2);
    }
    o3 = PyTuple_New(1);
    PyTuple_SetItem(o3,0,o);
    o2 = $result;
    $result = PySequence_Concat(o2,o3);
    Py_DECREF(o2);
    Py_DECREF(o3);
  }
}

%typemap(check) unsigned char *OUTPUT {
  /* nasty hack */
#ifdef __cplusplus
   $1 = ($1_ltype) new char[arg5];
#else
   $1 = ($1_ltype) malloc(arg5);
#endif
   if ($1 == NULL) SWIG_fail;
}

%typemap(argout,fragment="t_output_helper") unsigned char *OUTPUT {
   PyObject *o;
   o = SWIG_FromCharPtrAndSize($1, arg5);
   $result = t_output_helper($result,o);
#ifdef __cplusplus
   delete [] $1;
#else
   free($1);
#endif
}

#ifdef WIN32
typedef unsigned __int64 LONGUINT64;
typedef __int64          LONGINT64;
#else
typedef unsigned long long LONGUINT64;
typedef long long          LONGINT64;
#endif

/* the two available spaces in a CHM file                      */
/* N.B.: The format supports arbitrarily many spaces, but only */
/*       two appear to be used at present.                     */
#define CHM_UNCOMPRESSED (0)
#define CHM_COMPRESSED   (1)

/* structure representing an ITS (CHM) file stream             */
struct chmFile;

/* structure representing an element from an ITS file stream   */
struct chmUnitInfo
{
    LONGUINT64         start;
    LONGUINT64         length;
    int                space;
    char               path[CHM_MAX_PATHLEN+1];
};

/* open an ITS archive */
struct chmFile* chm_open(const char *filename);

/* close an ITS archive */
void chm_close(struct chmFile *h);

/* methods for ssetting tuning parameters for particular file */
#define CHM_PARAM_MAX_BLOCKS_CACHED 0
void chm_set_param(struct chmFile *h,
                   int paramType,
                   int paramVal);

/* resolve a particular object from the archive */
#define CHM_RESOLVE_SUCCESS (0)
#define CHM_RESOLVE_FAILURE (1)
int chm_resolve_object(struct chmFile *h,
                       const char *objPath,
                       struct chmUnitInfo *OutValue);

/* retrieve part of an object from the archive */
LONGINT64 chm_retrieve_object(struct chmFile *h,
                              struct chmUnitInfo *ui,
                              unsigned char *OUTPUT,
                              LONGUINT64 addr,
                              LONGINT64 len);

/* enumerate the objects in the .chm archive */
typedef int (*CHM_ENUMERATOR)(struct chmFile *h,
                              struct chmUnitInfo *ui,
                              void *context);
#define CHM_ENUMERATE_NORMAL    (1)
#define CHM_ENUMERATE_META      (2)
#define CHM_ENUMERATE_SPECIAL   (4)
#define CHM_ENUMERATE_FILES     (8)
#define CHM_ENUMERATE_DIRS      (16)
#define CHM_ENUMERATE_ALL       (31)
#define CHM_ENUMERATOR_FAILURE  (0)
#define CHM_ENUMERATOR_CONTINUE (1)
#define CHM_ENUMERATOR_SUCCESS  (2)
int chm_enumerate(struct chmFile *h,
                  int what,
                  CHM_ENUMERATOR e,
                  void *context);

int chm_enumerate_dir(struct chmFile *h,
                      const char *prefix,
                      int what,
                      CHM_ENUMERATOR e,
                      void *context);
