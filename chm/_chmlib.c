#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "chmlib_search.h"
#include <chm_lib.h>

#define CHMFILE_CAPSULE_NAME "C.chmFile"
#define CHMFILE_CLOSED ((void *)0x1)

#if PY_MAJOR_VERSION < 3
#define YF "s"
#else
#define YF "y"
#endif

static struct chmFile *chmlib_get_chmfile(PyObject *chmfile_capsule) {
  if (!PyCapsule_IsValid(chmfile_capsule, CHMFILE_CAPSULE_NAME)) {
    PyErr_SetString(PyExc_ValueError, "Expected valid chmlib object");
    return NULL;
  }

  struct chmFile *chmfile = (struct chmFile *)PyCapsule_GetPointer(
      chmfile_capsule, CHMFILE_CAPSULE_NAME);

  if (chmfile == CHMFILE_CLOSED) {
    PyErr_SetString(PyExc_RuntimeError, "chmlib object is closed");
    return NULL;
  }

  return chmfile;
}

static void chmlib_chmfile_capsule_destructor(PyObject *chmfile_capsule) {
  struct chmFile *chmfile = chmlib_get_chmfile(chmfile_capsule);
  if (!chmfile) {
    PyErr_Clear();
    return;
  }

  chm_close(chmfile);
  PyCapsule_SetPointer(chmfile_capsule, CHMFILE_CLOSED);
}

static PyObject *chmlib_chm_open(PyObject *self, PyObject *args) {
  const char *filename;
  if (!PyArg_ParseTuple(args, YF ":chmlib_chm_open", &filename))
    return NULL;

  struct chmFile *chmfile = chm_open(filename);
  if (chmfile == NULL)
    Py_RETURN_NONE;

  return PyCapsule_New(chmfile, CHMFILE_CAPSULE_NAME,
                       chmlib_chmfile_capsule_destructor);
}

static PyObject *chmlib_chm_close(PyObject *self, PyObject *args) {
  PyObject *chmfile_capsule;
  if (!PyArg_ParseTuple(args, "O:chmlib_chm_close", &chmfile_capsule))
    return NULL;

  chmlib_chmfile_capsule_destructor(chmfile_capsule);

  Py_RETURN_NONE;
}

static PyObject *chmlib_chm_set_param(PyObject *self, PyObject *args) {
  PyObject *chmfile_capsule;
  long param_type, param_val;

  if (!PyArg_ParseTuple(args, "Oii:chmlib_chm_set_param", &chmfile_capsule,
                        &param_type, &param_val))
    return NULL;

  struct chmFile *chmfile = chmlib_get_chmfile(chmfile_capsule);
  if (!chmfile)
    return NULL;

  // It's the only available parameter, and it's not going to change any time
  // soon.
  if (param_type != 0) {
    PyErr_Format(PyExc_ValueError,
                 "Expected CHM_PARAM_MAX_BLOCKS_CACHED (0), got %ld",
                 param_type);
    return NULL;
  }

  // The value for CHM_PARAM_MAX_BLOCKS_CACHED parameter ultimately gets
  // assigned to Int32 cache_num_blocks
  if (param_val < 0 || param_val > 0x7fffffff) {
    PyErr_Format(PyExc_ValueError, "Expected value 0..2147483647, got %ld",
                 param_val);
    return NULL;
  }

  chm_set_param(chmfile, (int)param_type, (int)param_val);

  Py_RETURN_NONE;
}

struct chmlib_enumerator_context {
  PyObject *chmfile_capsule;
  PyObject *py_enumerator;
  PyObject *py_context;

  int has_error;
};

static PyObject *chmUnitInfoTuple(struct chmUnitInfo *ui) {
  return Py_BuildValue("(KKii" YF ")", ui->start, ui->length, ui->space, ui->flags,
                       ui->path);
}

static int chmlib_chm_enumerator(struct chmFile *h, struct chmUnitInfo *ui,
                                 void *context) {
  struct chmlib_enumerator_context *ctx = context;
  long ret;

  PyObject *arglist = Py_BuildValue("(OOO)", ctx->chmfile_capsule,
                                    chmUnitInfoTuple(ui), ctx->py_context);
  PyObject *result = PyObject_CallObject(ctx->py_enumerator, arglist);
  Py_DECREF(arglist);

  if (result == NULL)
    goto fail;

  if (result == Py_None) {
    Py_DECREF(result);
    return CHM_ENUMERATOR_CONTINUE;
  }

  if (
#if PY_MAJOR_VERSION < 3
      !PyInt_Check(result) &&
#endif
      !PyLong_Check(result)) {
    PyErr_Format(PyExc_RuntimeError,
                 "chm_enumerate callback is expected to return "
                 "integer or None, returned %R",
                 result);
    goto fail2;
  }

  ret = PyLong_AsLong(result);
  if (ret == -1 && PyErr_Occurred() != NULL)
    goto fail2;

  return (int)ret;

fail2:
  Py_DECREF(result);

fail:
  ctx->has_error = 1;
  return CHM_ENUMERATOR_FAILURE;
}

static PyObject *chmlib_chm_enumerate_dir(PyObject *self, PyObject *args) {
  PyObject *chmfile_capsule;
  const char *prefix;
  int what;
  PyObject *enumerator;
  PyObject *context;
  int res;

  if (!PyArg_ParseTuple(args, "O" YF "iOO:chmlib_chm_enumerate", &chmfile_capsule,
                        &prefix, &what, &enumerator, &context))
    return NULL;

  struct chmFile *chmfile = chmlib_get_chmfile(chmfile_capsule);
  if (!chmfile)
    return NULL;

  if (!PyCallable_Check(enumerator)) {
    PyErr_Format(PyExc_TypeError, "A callable is expected for callback, got %R",
                 enumerator);
    return NULL;
  }

  struct chmlib_enumerator_context ctx = {
      .chmfile_capsule = chmfile_capsule,
      .py_enumerator = enumerator,
      .py_context = context,
  };

  res = chm_enumerate_dir(chmfile, prefix, what, chmlib_chm_enumerator, &ctx);

  if (ctx.has_error)
    return NULL;

  return PyLong_FromLong(res);
}

static PyObject *chmlib_chm_enumerate(PyObject *self, PyObject *args) {
  PyObject *chmfile_capsule;
  int what;
  PyObject *enumerator;
  PyObject *context;
  int res;

  if (!PyArg_ParseTuple(args, "OiOO:chmlib_chm_enumerate", &chmfile_capsule,
                        &what, &enumerator, &context))
    return NULL;

  struct chmFile *chmfile = chmlib_get_chmfile(chmfile_capsule);
  if (!chmfile)
    return NULL;

  if (!PyCallable_Check(enumerator)) {
    PyErr_Format(PyExc_TypeError, "A callable is expected for callback, got %R",
                 enumerator);
    return NULL;
  }

  struct chmlib_enumerator_context ctx = {
      .chmfile_capsule = chmfile_capsule,
      .py_enumerator = enumerator,
      .py_context = context,
  };

  res = chm_enumerate(chmfile, what, chmlib_chm_enumerator, &ctx);

  if (ctx.has_error)
    return NULL;

  return PyLong_FromLong(res);
}

static PyObject *chmlib_chm_resolve_object(PyObject *self, PyObject *args) {
  PyObject *chmfile_capsule;
  const char *path;
  struct chmUnitInfo ui;

  if (!PyArg_ParseTuple(args, "O" YF ":chmlib_chm_resolve_object", &chmfile_capsule,
                        &path))
    return NULL;

  struct chmFile *chmfile = chmlib_get_chmfile(chmfile_capsule);
  if (!chmfile)
    return NULL;

  if (chm_resolve_object(chmfile, path, &ui) == CHM_RESOLVE_FAILURE) {
    Py_RETURN_NONE;
  }

  return chmUnitInfoTuple(&ui);
}

static PyObject *chmlib_chm_retrieve_object(PyObject *self, PyObject *args) {
  PyObject *chmfile_capsule;
  unsigned long long uistart;
  unsigned long long uilength;
  int uispace;
  unsigned long long offset;
  long long length;
  long long res;
  char *buf;
  PyObject *pybuf;

  if (!PyArg_ParseTuple(args, "OKKiKL:chmlib_chm_retrieve_object",
                        &chmfile_capsule, &uistart, &uilength, &uispace,
                        &offset, &length))
    return NULL;

  struct chmFile *chmfile = chmlib_get_chmfile(chmfile_capsule);
  if (!chmfile)
    return NULL;

  if (length < 0) {
    PyErr_Format(PyExc_ValueError,
                 "Expected non-negative object length, got %lld", length);
    return NULL;
  }

  pybuf = PyBytes_FromStringAndSize(NULL, (Py_ssize_t)length);
  if (!pybuf)
    return NULL;

  buf = PyBytes_AS_STRING(pybuf);

  struct chmUnitInfo ui = {
      .start = uistart,
      .length = uilength,
      .space = uispace,
  };

  res = chm_retrieve_object(chmfile, &ui, (unsigned char *)buf, offset, length);

  if (res == 0) {
    Py_DECREF(pybuf);
    Py_RETURN_NONE;
  }

  if (res != length) {
    // error checking is not needed: pybuf is set to NULL in case of error
    _PyBytes_Resize(&pybuf, (Py_ssize_t)res);
  }

  return pybuf;
}

typedef struct {
  PyObject *cb;
  int has_error;
} search_ctx;

static int _search_cb(const char *topic, const char *url, void *context) {
  search_ctx *ctx = context;

  PyObject *arglist = Py_BuildValue("(" YF YF ")", topic, url);
  PyObject *result = PyObject_CallObject(ctx->cb, arglist);
  Py_DECREF(arglist);

  if (result == NULL) {
    ctx->has_error = 1;
    return -1;
  }

  Py_DECREF(result);
  return 0;
}

static PyObject *chmlib_search(PyObject *self, PyObject *args) {
  PyObject *chmfile_capsule;
  const char *text;
  int whole_words;
  int titles_only;
  PyObject *pycb;
  int ret;

  if (!PyArg_ParseTuple(args, "O" YF "iiO:chmlib_search", &chmfile_capsule, &text,
                        &whole_words, &titles_only, &pycb))
    return NULL;

  struct chmFile *chmfile = chmlib_get_chmfile(chmfile_capsule);
  if (!chmfile)
    return NULL;

  if (!PyCallable_Check(pycb)) {
    PyErr_Format(PyExc_TypeError, "A callable is expected for callback, got %R",
                 pycb);
    return NULL;
  }

  search_ctx ctx = {
      .cb = pycb,
  };

  ret = search(chmfile, text, whole_words, titles_only, _search_cb, &ctx);

  if (ctx.has_error)
    return NULL;

  return Py_BuildValue("i", ret);
}

static PyMethodDef chmlib_methods[] = {
    {"chm_open", chmlib_chm_open, METH_VARARGS, "Open a CHM file"},
    {"chm_close", chmlib_chm_close, METH_VARARGS, "Open the CHM file"},
    {"chm_enumerate", chmlib_chm_enumerate, METH_VARARGS,
     "Enumerate objects in CHM file"},
    {"chm_set_param", chmlib_chm_set_param, METH_VARARGS,
     "Set parameters of CHM object"},
    {"chm_enumerate_dir", chmlib_chm_enumerate_dir, METH_VARARGS,
     "Enumerate objects in CHM file"},
    {"chm_resolve_object", chmlib_chm_resolve_object, METH_VARARGS,
     "Find the object by path in CHM file"},
    {"chm_retrieve_object", chmlib_chm_retrieve_object, METH_VARARGS,
     "Get the object's content"},
    {"search", chmlib_search, METH_VARARGS, "Search the CHM"},
};

#if PY_MAJOR_VERSION < 3

void init_chmlib(void) { Py_InitModule("_chmlib", chmlib_methods); }

#else

static struct PyModuleDef chmlib_module = {
    PyModuleDef_HEAD_INIT, "_chmlib", NULL, -1, chmlib_methods,
};

PyMODINIT_FUNC PyInit__chmlib(void) { return PyModule_Create(&chmlib_module); }

#endif
