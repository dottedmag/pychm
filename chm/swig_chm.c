/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 1.3.18
 * 
 * This file is not intended to be easily readable and contains a number of 
 * coding conventions designed to improve portability and efficiency. Do not make
 * changes to this file unless you know what you are doing--modify the SWIG 
 * interface file instead. 
 * ----------------------------------------------------------------------------- */

#define SWIGPYTHON

#include "Python.h"

/***********************************************************************
 * common.swg
 *
 *     This file contains generic SWIG runtime support for pointer
 *     type checking as well as a few commonly used macros to control
 *     external linkage.
 *
 * Author : David Beazley (beazley@cs.uchicago.edu)
 *
 * Copyright (c) 1999-2000, The University of Chicago
 * 
 * This file may be freely redistributed without license or fee provided
 * this copyright message remains intact.
 ************************************************************************/

#include <string.h>

#if defined(_WIN32) || defined(__WIN32__)
#       if defined(_MSC_VER)
#               if defined(STATIC_LINKED)
#                       define SWIGEXPORT(a) a
#                       define SWIGIMPORT(a) extern a
#               else
#                       define SWIGEXPORT(a) __declspec(dllexport) a
#                       define SWIGIMPORT(a) extern a
#               endif
#       else
#               if defined(__BORLANDC__)
#                       define SWIGEXPORT(a) a _export
#                       define SWIGIMPORT(a) a _export
#               else
#                       define SWIGEXPORT(a) a
#                       define SWIGIMPORT(a) a
#               endif
#       endif
#else
#       define SWIGEXPORT(a) a
#       define SWIGIMPORT(a) a
#endif

#ifdef SWIG_GLOBAL
#define SWIGRUNTIME(a) SWIGEXPORT(a)
#else
#define SWIGRUNTIME(a) static a
#endif

#ifdef __cplusplus
extern "C" {
#endif

typedef void *(*swig_converter_func)(void *);
typedef struct swig_type_info *(*swig_dycast_func)(void **);

typedef struct swig_type_info {
  const char             *name;                 
  swig_converter_func     converter;
  const char             *str;
  void                   *clientdata;	
  swig_dycast_func        dcast;
  struct swig_type_info  *next;
  struct swig_type_info  *prev;
} swig_type_info;

#ifdef SWIG_NOINCLUDE

SWIGIMPORT(swig_type_info *) SWIG_TypeRegister(swig_type_info *);
SWIGIMPORT(swig_type_info *) SWIG_TypeCheck(char *c, swig_type_info *);
SWIGIMPORT(void *)           SWIG_TypeCast(swig_type_info *, void *);
SWIGIMPORT(swig_type_info *) SWIG_TypeDynamicCast(swig_type_info *, void **);
SWIGIMPORT(const char *)     SWIG_TypeName(const swig_type_info *);
SWIGIMPORT(swig_type_info *) SWIG_TypeQuery(const char *);
SWIGIMPORT(void)             SWIG_TypeClientData(swig_type_info *, void *);

#else

static swig_type_info *swig_type_list = 0;

/* Register a type mapping with the type-checking */
SWIGRUNTIME(swig_type_info *)
SWIG_TypeRegister(swig_type_info *ti)
{
  swig_type_info *tc, *head, *ret, *next;
  /* Check to see if this type has already been registered */
  tc = swig_type_list;
  while (tc) {
    if (strcmp(tc->name, ti->name) == 0) {
      /* Already exists in the table.  Just add additional types to the list */
      if (tc->clientdata) ti->clientdata = tc->clientdata;	
      head = tc;
      next = tc->next;
      goto l1;
    }
    tc = tc->prev;
  }
  head = ti;
  next = 0;

  /* Place in list */
  ti->prev = swig_type_list;
  swig_type_list = ti;

  /* Build linked lists */
 l1:
  ret = head;
  tc = ti + 1;
  /* Patch up the rest of the links */
  while (tc->name) {
    head->next = tc;
    tc->prev = head;
    head = tc;
    tc++;
  }
  if (next) next->prev = head;  /**/
  head->next = next;
  return ret;
}

/* Check the typename */
SWIGRUNTIME(swig_type_info *) 
SWIG_TypeCheck(char *c, swig_type_info *ty)
{
  swig_type_info *s;
  if (!ty) return 0;        /* Void pointer */
  s = ty->next;             /* First element always just a name */
  do {
    if (strcmp(s->name,c) == 0) {
      if (s == ty->next) return s;
      /* Move s to the top of the linked list */
      s->prev->next = s->next;
      if (s->next) {
	s->next->prev = s->prev;
      }
      /* Insert s as second element in the list */
      s->next = ty->next;
      if (ty->next) ty->next->prev = s;
      ty->next = s;
      s->prev = ty;  /**/
      return s;
    }
    s = s->next;
  } while (s && (s != ty->next));
  return 0;
}

/* Cast a pointer up an inheritance hierarchy */
SWIGRUNTIME(void *) 
SWIG_TypeCast(swig_type_info *ty, void *ptr) 
{
  if ((!ty) || (!ty->converter)) return ptr;
  return (*ty->converter)(ptr);
}

/* Dynamic pointer casting. Down an inheritance hierarchy */
SWIGRUNTIME(swig_type_info *) 
SWIG_TypeDynamicCast(swig_type_info *ty, void **ptr) 
{
  swig_type_info *lastty = ty;
  if (!ty || !ty->dcast) return ty;
  while (ty && (ty->dcast)) {
     ty = (*ty->dcast)(ptr);
     if (ty) lastty = ty;
  }
  return lastty;
}

/* Return the name associated with this type */
SWIGRUNTIME(const char *)
SWIG_TypeName(const swig_type_info *ty) {
  return ty->name;
}

/* Search for a swig_type_info structure */
SWIGRUNTIME(swig_type_info *)
SWIG_TypeQuery(const char *name) {
  swig_type_info *ty = swig_type_list;
  while (ty) {
    if (ty->str && (strcmp(name,ty->str) == 0)) return ty;
    if (ty->name && (strcmp(name,ty->name) == 0)) return ty;
    ty = ty->prev;
  }
  return 0;
}

/* Set the clientdata field for a type */
SWIGRUNTIME(void)
SWIG_TypeClientData(swig_type_info *ti, void *clientdata) {
  swig_type_info *tc, *equiv;
  if (ti->clientdata == clientdata) return;
  ti->clientdata = clientdata;
  equiv = ti->next;
  while (equiv) {
    if (!equiv->converter) {
      tc = swig_type_list;
      while (tc) {
	if ((strcmp(tc->name, equiv->name) == 0))
	  SWIG_TypeClientData(tc,clientdata);
	tc = tc->prev;
      }
    }
    equiv = equiv->next;
  }
}
#endif

#ifdef __cplusplus
}

#endif

/***********************************************************************
 * python.swg
 *
 *     This file contains the runtime support for Python modules
 *     and includes code for managing global variables and pointer
 *     type checking.
 *
 * Author : David Beazley (beazley@cs.uchicago.edu)
 ************************************************************************/

#include "Python.h"

#ifdef __cplusplus
extern "C" {
#endif

#define SWIG_PY_INT     1
#define SWIG_PY_FLOAT   2
#define SWIG_PY_STRING  3
#define SWIG_PY_POINTER 4
#define SWIG_PY_BINARY  5

/* Flags for pointer conversion */

#define SWIG_POINTER_EXCEPTION     0x1
#define SWIG_POINTER_DISOWN        0x2

/* Exception handling in wrappers */
#define SWIG_fail   goto fail

/* Constant information structure */
typedef struct swig_const_info {
    int type;
    char *name;
    long lvalue;
    double dvalue;
    void   *pvalue;
    swig_type_info **ptype;
} swig_const_info;

#ifdef SWIG_NOINCLUDE

SWIGEXPORT(PyObject *)        SWIG_newvarlink(void);
SWIGEXPORT(void)              SWIG_addvarlink(PyObject *, char *, PyObject *(*)(void), int (*)(PyObject *));
SWIGEXPORT(int)               SWIG_ConvertPtr(PyObject *, void **, swig_type_info *, int);
SWIGEXPORT(int)               SWIG_ConvertPacked(PyObject *, void *, int sz, swig_type_info *, int);
SWIGEXPORT(char *)            SWIG_PackData(char *c, void *, int);
SWIGEXPORT(char *)            SWIG_UnpackData(char *c, void *, int);
SWIGEXPORT(PyObject *)        SWIG_NewPointerObj(void *, swig_type_info *,int own);
SWIGEXPORT(PyObject *)        SWIG_NewPackedObj(void *, int sz, swig_type_info *);
SWIGEXPORT(void)              SWIG_InstallConstants(PyObject *d, swig_const_info constants[]);
#else

/* -----------------------------------------------------------------------------
 * global variable support code.
 * ----------------------------------------------------------------------------- */

typedef struct swig_globalvar {   
  char       *name;                  /* Name of global variable */
  PyObject *(*get_attr)(void);       /* Return the current value */
  int       (*set_attr)(PyObject *); /* Set the value */
  struct swig_globalvar *next;
} swig_globalvar;

typedef struct swig_varlinkobject {
  PyObject_HEAD
  swig_globalvar *vars;
} swig_varlinkobject;

static PyObject *
swig_varlink_repr(swig_varlinkobject *v) {
  v = v;
  return PyString_FromString("<Global variables>");
}

static int
swig_varlink_print(swig_varlinkobject *v, FILE *fp, int flags) {
  swig_globalvar  *var;
  flags = flags;
  fprintf(fp,"Global variables { ");
  for (var = v->vars; var; var=var->next) {
    fprintf(fp,"%s", var->name);
    if (var->next) fprintf(fp,", ");
  }
  fprintf(fp," }\n");
  return 0;
}

static PyObject *
swig_varlink_getattr(swig_varlinkobject *v, char *n) {
  swig_globalvar *var = v->vars;
  while (var) {
    if (strcmp(var->name,n) == 0) {
      return (*var->get_attr)();
    }
    var = var->next;
  }
  PyErr_SetString(PyExc_NameError,"Unknown C global variable");
  return NULL;
}

static int
swig_varlink_setattr(swig_varlinkobject *v, char *n, PyObject *p) {
  swig_globalvar *var = v->vars;
  while (var) {
    if (strcmp(var->name,n) == 0) {
      return (*var->set_attr)(p);
    }
    var = var->next;
  }
  PyErr_SetString(PyExc_NameError,"Unknown C global variable");
  return 1;
}

statichere PyTypeObject varlinktype = {
  PyObject_HEAD_INIT(0)              
  0,
  (char *)"swigvarlink",                      /* Type name    */
  sizeof(swig_varlinkobject),         /* Basic size   */
  0,                                  /* Itemsize     */
  0,                                  /* Deallocator  */ 
  (printfunc) swig_varlink_print,     /* Print        */
  (getattrfunc) swig_varlink_getattr, /* get attr     */
  (setattrfunc) swig_varlink_setattr, /* Set attr     */
  0,                                  /* tp_compare   */
  (reprfunc) swig_varlink_repr,       /* tp_repr      */    
  0,                                  /* tp_as_number */
  0,                                  /* tp_as_mapping*/
  0,                                  /* tp_hash      */
};

/* Create a variable linking object for use later */
SWIGRUNTIME(PyObject *)
SWIG_newvarlink(void) {
  swig_varlinkobject *result = 0;
  result = PyMem_NEW(swig_varlinkobject,1);
  varlinktype.ob_type = &PyType_Type;    /* Patch varlinktype into a PyType */
  result->ob_type = &varlinktype;
  result->vars = 0;
  result->ob_refcnt = 0;
  Py_XINCREF((PyObject *) result);
  return ((PyObject*) result);
}

SWIGRUNTIME(void)
SWIG_addvarlink(PyObject *p, char *name,
	   PyObject *(*get_attr)(void), int (*set_attr)(PyObject *p)) {
  swig_varlinkobject *v;
  swig_globalvar *gv;
  v= (swig_varlinkobject *) p;
  gv = (swig_globalvar *) malloc(sizeof(swig_globalvar));
  gv->name = (char *) malloc(strlen(name)+1);
  strcpy(gv->name,name);
  gv->get_attr = get_attr;
  gv->set_attr = set_attr;
  gv->next = v->vars;
  v->vars = gv;
}

/* Pack binary data into a string */
SWIGRUNTIME(char *)
SWIG_PackData(char *c, void *ptr, int sz) {
  static char hex[17] = "0123456789abcdef";
  int i;
  unsigned char *u = (unsigned char *) ptr;
  register unsigned char uu;
  for (i = 0; i < sz; i++,u++) {
    uu = *u;
    *(c++) = hex[(uu & 0xf0) >> 4];
    *(c++) = hex[uu & 0xf];
  }
  return c;
}

/* Unpack binary data from a string */
SWIGRUNTIME(char *)
SWIG_UnpackData(char *c, void *ptr, int sz) {
  register unsigned char uu = 0;
  register int d;
  unsigned char *u = (unsigned char *) ptr;
  int i;
  for (i = 0; i < sz; i++, u++) {
    d = *(c++);
    if ((d >= '0') && (d <= '9'))
      uu = ((d - '0') << 4);
    else if ((d >= 'a') && (d <= 'f'))
      uu = ((d - ('a'-10)) << 4);
    d = *(c++);
    if ((d >= '0') && (d <= '9'))
      uu |= (d - '0');
    else if ((d >= 'a') && (d <= 'f'))
      uu |= (d - ('a'-10));
    *u = uu;
  }
  return c;
}

/* Convert a pointer value */
SWIGRUNTIME(int)
SWIG_ConvertPtr(PyObject *obj, void **ptr, swig_type_info *ty, int flags) {
  swig_type_info *tc;
  char  *c;
  static PyObject *SWIG_this = 0;
  int    newref = 0;
  PyObject  *pyobj = 0;

  if (!obj) return 0;
  if (obj == Py_None) {
    *ptr = 0;
    return 0;
  }
#ifdef SWIG_COBJECT_TYPES
  if (!(PyCObject_Check(obj))) {
    if (!SWIG_this)
      SWIG_this = PyString_FromString("this");
    pyobj = obj;
    obj = PyObject_GetAttr(obj,SWIG_this);
    newref = 1;
    if (!obj) goto type_error;
    if (!PyCObject_Check(obj)) {
      Py_DECREF(obj);
      goto type_error;
    }
  }  
  *ptr = PyCObject_AsVoidPtr(obj);
  c = (char *) PyCObject_GetDesc(obj);
  if (newref) Py_DECREF(obj);
  goto cobject;
#else
  if (!(PyString_Check(obj))) {
    if (!SWIG_this)
      SWIG_this = PyString_FromString("this");
    pyobj = obj;
    obj = PyObject_GetAttr(obj,SWIG_this);
    newref = 1;
    if (!obj) goto type_error;
    if (!PyString_Check(obj)) {
      Py_DECREF(obj);
      goto type_error;
    }
  } 
  c = PyString_AsString(obj);
  /* Pointer values must start with leading underscore */
  if (*c != '_') {
    *ptr = (void *) 0;
    if (strcmp(c,"NULL") == 0) {
      if (newref) { Py_DECREF(obj); }
      return 0;
    } else {
      if (newref) { Py_DECREF(obj); }
      goto type_error;
    }
  }
  c++;
  c = SWIG_UnpackData(c,ptr,sizeof(void *));
  if (newref) { Py_DECREF(obj); }
#endif

#ifdef SWIG_COBJECT_TYPES
cobject:
#endif

  if (ty) {
    tc = SWIG_TypeCheck(c,ty);
    if (!tc) goto type_error;
    *ptr = SWIG_TypeCast(tc,(void*) *ptr);
  }

  if ((pyobj) && (flags & SWIG_POINTER_DISOWN)) {
      PyObject *zero = PyInt_FromLong(0);
      PyObject_SetAttrString(pyobj,(char*)"thisown",zero);
      Py_DECREF(zero);
  }
  return 0;

type_error:
  if (flags & SWIG_POINTER_EXCEPTION) {
    if (ty) {
      char *temp = (char *) malloc(64+strlen(ty->name));
      sprintf(temp,"Type error. Expected %s", ty->name);
      PyErr_SetString(PyExc_TypeError, temp);
      free((char *) temp);
    } else {
      PyErr_SetString(PyExc_TypeError,"Expected a pointer");
    }
  }
  return -1;
}

/* Convert a packed value value */
SWIGRUNTIME(int)
SWIG_ConvertPacked(PyObject *obj, void *ptr, int sz, swig_type_info *ty, int flags) {
  swig_type_info *tc;
  char  *c;

  if ((!obj) || (!PyString_Check(obj))) goto type_error;
  c = PyString_AsString(obj);
  /* Pointer values must start with leading underscore */
  if (*c != '_') goto type_error;
  c++;
  c = SWIG_UnpackData(c,ptr,sz);
  if (ty) {
    tc = SWIG_TypeCheck(c,ty);
    if (!tc) goto type_error;
  }
  return 0;

type_error:

  if (flags) {
    if (ty) {
      char *temp = (char *) malloc(64+strlen(ty->name));
      sprintf(temp,"Type error. Expected %s", ty->name);
      PyErr_SetString(PyExc_TypeError, temp);
      free((char *) temp);
    } else {
      PyErr_SetString(PyExc_TypeError,"Expected a pointer");
    }
  }
  return -1;
}

/* Create a new pointer object */
SWIGRUNTIME(PyObject *)
SWIG_NewPointerObj(void *ptr, swig_type_info *type, int own) {
  PyObject *robj;
  if (!ptr) {
    Py_INCREF(Py_None);
    return Py_None;
  }
#ifdef SWIG_COBJECT_TYPES
  robj = PyCObject_FromVoidPtrAndDesc((void *) ptr, (char *) type->name, NULL);
#else
  {
    char result[1024];
    char *r = result;
    *(r++) = '_';
    r = SWIG_PackData(r,&ptr,sizeof(void *));
    strcpy(r,type->name);
    robj = PyString_FromString(result);
  }
#endif
  if (!robj || (robj == Py_None)) return robj;
  if (type->clientdata) {
    PyObject *inst;
    PyObject *args = Py_BuildValue((char*)"(O)", robj);
    Py_DECREF(robj);
    inst = PyObject_CallObject((PyObject *) type->clientdata, args);
    Py_DECREF(args);
    if (inst) {
      if (own) {
	PyObject *n = PyInt_FromLong(1);
	PyObject_SetAttrString(inst,(char*)"thisown",n);
	Py_DECREF(n);
      }
      robj = inst;
    }
  }
  return robj;
}

SWIGRUNTIME(PyObject *)
SWIG_NewPackedObj(void *ptr, int sz, swig_type_info *type) {
  char result[1024];
  char *r = result;
  if ((2*sz + 1 + strlen(type->name)) > 1000) return 0;
  *(r++) = '_';
  r = SWIG_PackData(r,ptr,sz);
  strcpy(r,type->name);
  return PyString_FromString(result);
}

/* Install Constants */
SWIGRUNTIME(void)
SWIG_InstallConstants(PyObject *d, swig_const_info constants[]) {
  int i;
  PyObject *obj;
  for (i = 0; constants[i].type; i++) {
    switch(constants[i].type) {
    case SWIG_PY_INT:
      obj = PyInt_FromLong(constants[i].lvalue);
      break;
    case SWIG_PY_FLOAT:
      obj = PyFloat_FromDouble(constants[i].dvalue);
      break;
    case SWIG_PY_STRING:
      obj = PyString_FromString((char *) constants[i].pvalue);
      break;
    case SWIG_PY_POINTER:
      obj = SWIG_NewPointerObj(constants[i].pvalue, *(constants[i]).ptype,0);
      break;
    case SWIG_PY_BINARY:
      obj = SWIG_NewPackedObj(constants[i].pvalue, constants[i].lvalue, *(constants[i].ptype));
      break;
    default:
      obj = 0;
      break;
    }
    if (obj) {
      PyDict_SetItemString(d,constants[i].name,obj);
      Py_DECREF(obj);
    }
  }
}

#endif

#ifdef __cplusplus
}
#endif








/* -------- TYPES TABLE (BEGIN) -------- */

#define  SWIGTYPE_p_chmUnitInfo swig_types[0] 
#define  SWIGTYPE_p_unsigned_char swig_types[1] 
#define  SWIGTYPE_p_char swig_types[2] 
#define  SWIGTYPE_CHM_ENUMERATOR swig_types[3] 
#define  SWIGTYPE_p_chmFile swig_types[4] 
static swig_type_info *swig_types[6];

/* -------- TYPES TABLE (END) -------- */


/*-----------------------------------------------
              @(target):= _chmlib.so
  ------------------------------------------------*/
#define SWIG_init    init_chmlib

#define SWIG_name    "_chmlib"

/*
 Copyright (C) 2003 Rubens Ramos <rubens_ramos@yahoo.com>

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
    py_c  = PyCObject_AsVoidPtr(context);

    /* Time to call the callback */
    arglist = Py_BuildValue("(OOO)", py_h, py_ui, py_c);
    if (arglist) {
      result = PyEval_CallObject(my_callback, arglist);
      Py_DECREF(arglist);
      Py_DECREF(result);
      
      Py_DECREF(py_h);
      Py_DECREF(py_ui);
      
      if (result == NULL) {
        return 0; /* Pass error back */
      } else {
        return 1;
      }
    } else
      return 0;
 }


static PyObject* t_output_helper(PyObject* target, PyObject* o) {
    PyObject*   o2;
    PyObject*   o3;

    if (!target) {                   
        target = o;
    } else if (target == Py_None) {  
        Py_DECREF(Py_None);
        target = o;
    } else {                         
        if (!PyTuple_Check(target)) {
            o2 = target;
            target = PyTuple_New(1);
            PyTuple_SetItem(target, 0, o2);
        }
        o3 = PyTuple_New(1);            
        PyTuple_SetItem(o3, 0, o);      

        o2 = target;
        target = PySequence_Concat(o2, o3); 
        Py_DECREF(o2);                      
        Py_DECREF(o3);
    }
    return target;
}

#ifdef __cplusplus
extern "C" {
#endif
static PyObject *_wrap_chmUnitInfo_start_set(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmUnitInfo *arg1 = (struct chmUnitInfo *) 0 ;
    LONGUINT64 arg2 ;
    PyObject * obj0 = 0 ;
    PyObject * obj1 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"OO:chmUnitInfo_start_set",&obj0,&obj1)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmUnitInfo,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    arg2 = (LONGUINT64) PyLong_AsUnsignedLongLong(obj1);
    if (PyErr_Occurred()) SWIG_fail;
    if (arg1) (arg1)->start = arg2;
    
    Py_INCREF(Py_None); resultobj = Py_None;
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chmUnitInfo_start_get(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmUnitInfo *arg1 = (struct chmUnitInfo *) 0 ;
    LONGUINT64 result;
    PyObject * obj0 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"O:chmUnitInfo_start_get",&obj0)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmUnitInfo,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    result = (LONGUINT64) ((arg1)->start);
    
    resultobj = PyLong_FromUnsignedLongLong(result);
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chmUnitInfo_length_set(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmUnitInfo *arg1 = (struct chmUnitInfo *) 0 ;
    LONGUINT64 arg2 ;
    PyObject * obj0 = 0 ;
    PyObject * obj1 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"OO:chmUnitInfo_length_set",&obj0,&obj1)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmUnitInfo,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    arg2 = (LONGUINT64) PyLong_AsUnsignedLongLong(obj1);
    if (PyErr_Occurred()) SWIG_fail;
    if (arg1) (arg1)->length = arg2;
    
    Py_INCREF(Py_None); resultobj = Py_None;
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chmUnitInfo_length_get(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmUnitInfo *arg1 = (struct chmUnitInfo *) 0 ;
    LONGUINT64 result;
    PyObject * obj0 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"O:chmUnitInfo_length_get",&obj0)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmUnitInfo,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    result = (LONGUINT64) ((arg1)->length);
    
    resultobj = PyLong_FromUnsignedLongLong(result);
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chmUnitInfo_space_set(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmUnitInfo *arg1 = (struct chmUnitInfo *) 0 ;
    int arg2 ;
    PyObject * obj0 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"Oi:chmUnitInfo_space_set",&obj0,&arg2)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmUnitInfo,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    if (arg1) (arg1)->space = arg2;
    
    Py_INCREF(Py_None); resultobj = Py_None;
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chmUnitInfo_space_get(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmUnitInfo *arg1 = (struct chmUnitInfo *) 0 ;
    int result;
    PyObject * obj0 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"O:chmUnitInfo_space_get",&obj0)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmUnitInfo,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    result = (int) ((arg1)->space);
    
    resultobj = PyInt_FromLong((long)result);
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chmUnitInfo_path_set(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmUnitInfo *arg1 = (struct chmUnitInfo *) 0 ;
    char *arg2 ;
    PyObject * obj0 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"Os:chmUnitInfo_path_set",&obj0,&arg2)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmUnitInfo,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    {
        if (arg2) strncpy(arg1->path,arg2,256+1);
        else arg1->path[0] = 0;
    }
    Py_INCREF(Py_None); resultobj = Py_None;
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chmUnitInfo_path_get(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmUnitInfo *arg1 = (struct chmUnitInfo *) 0 ;
    char *result;
    PyObject * obj0 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"O:chmUnitInfo_path_get",&obj0)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmUnitInfo,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    result = (char *)(char *) ((arg1)->path);
    
    resultobj = PyString_FromString(result);
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_new_chmUnitInfo(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmUnitInfo *result;
    
    if(!PyArg_ParseTuple(args,(char *)":new_chmUnitInfo")) goto fail;
    result = (struct chmUnitInfo *)(struct chmUnitInfo *) calloc(1, sizeof(struct chmUnitInfo));
    
    resultobj = SWIG_NewPointerObj((void *) result, SWIGTYPE_p_chmUnitInfo, 1);
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_delete_chmUnitInfo(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmUnitInfo *arg1 = (struct chmUnitInfo *) 0 ;
    PyObject * obj0 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"O:delete_chmUnitInfo",&obj0)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmUnitInfo,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    free((char *) arg1);
    
    Py_INCREF(Py_None); resultobj = Py_None;
    return resultobj;
    fail:
    return NULL;
}


static PyObject * chmUnitInfo_swigregister(PyObject *self, PyObject *args) {
    PyObject *obj;
    if (!PyArg_ParseTuple(args,(char*)"O", &obj)) return NULL;
    SWIG_TypeClientData(SWIGTYPE_p_chmUnitInfo, obj);
    Py_INCREF(obj);
    return Py_BuildValue((char *)"");
}
static PyObject *_wrap_chm_open(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    char *arg1 ;
    struct chmFile *result;
    
    if(!PyArg_ParseTuple(args,(char *)"s:chm_open",&arg1)) goto fail;
    result = (struct chmFile *)chm_open((char const *)arg1);
    
    resultobj = SWIG_NewPointerObj((void *) result, SWIGTYPE_p_chmFile, 0);
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chm_close(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmFile *arg1 = (struct chmFile *) 0 ;
    PyObject * obj0 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"O:chm_close",&obj0)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmFile,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    chm_close(arg1);
    
    Py_INCREF(Py_None); resultobj = Py_None;
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chm_set_param(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmFile *arg1 = (struct chmFile *) 0 ;
    int arg2 ;
    int arg3 ;
    PyObject * obj0 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"Oii:chm_set_param",&obj0,&arg2,&arg3)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmFile,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    chm_set_param(arg1,arg2,arg3);
    
    Py_INCREF(Py_None); resultobj = Py_None;
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chm_resolve_object(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmFile *arg1 = (struct chmFile *) 0 ;
    char *arg2 ;
    struct chmUnitInfo *arg3 = (struct chmUnitInfo *) 0 ;
    int result;
    struct chmUnitInfo *temp3 = (struct chmUnitInfo *) calloc(1, sizeof(struct chmUnitInfo)) ;
    PyObject * obj0 = 0 ;
    
    {
        arg3 = temp3;
    }
    if(!PyArg_ParseTuple(args,(char *)"Os:chm_resolve_object",&obj0,&arg2)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmFile,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    result = (int)chm_resolve_object(arg1,(char const *)arg2,arg3);
    
    resultobj = PyInt_FromLong((long)result);
    {
        PyObject *o, *o2, *o3;
        o = SWIG_NewPointerObj((void *) arg3, SWIGTYPE_p_chmUnitInfo, 1);
        if ((!resultobj) || (resultobj == Py_None)) {
            resultobj = o;
        }else {
            if (!PyTuple_Check(resultobj)) {
                PyObject *o2 = resultobj;
                resultobj = PyTuple_New(1);
                PyTuple_SetItem(resultobj,0,o2);
            }
            o3 = PyTuple_New(1);
            PyTuple_SetItem(o3,0,o);
            o2 = resultobj;
            resultobj = PySequence_Concat(o2,o3);
            Py_DECREF(o2);
            Py_DECREF(o3);
        }
    }
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chm_retrieve_object(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmFile *arg1 = (struct chmFile *) 0 ;
    struct chmUnitInfo *arg2 = (struct chmUnitInfo *) 0 ;
    unsigned char *arg3 = (unsigned char *) 0 ;
    LONGUINT64 arg4 ;
    LONGINT64 arg5 ;
    LONGINT64 result;
    unsigned char temp3 ;
    PyObject * obj0 = 0 ;
    PyObject * obj1 = 0 ;
    PyObject * obj2 = 0 ;
    PyObject * obj3 = 0 ;
    
    arg3 = &temp3;
    if(!PyArg_ParseTuple(args,(char *)"OOOO:chm_retrieve_object",&obj0,&obj1,&obj2,&obj3)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmFile,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    if ((SWIG_ConvertPtr(obj1,(void **) &arg2, SWIGTYPE_p_chmUnitInfo,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    arg4 = (LONGUINT64) PyLong_AsUnsignedLongLong(obj2);
    if (PyErr_Occurred()) SWIG_fail;
    arg5 = (LONGINT64) PyLong_AsLongLong(obj3);
    if (PyErr_Occurred()) SWIG_fail;
    {
        /* nasty hack */
        
        
        
        arg3 = (unsigned char *) malloc(arg5);
        
        if (arg3 == NULL) SWIG_fail;
    }
    result = (LONGINT64)chm_retrieve_object(arg1,arg2,arg3,arg4,arg5);
    
    resultobj = PyLong_FromLongLong(result);
    {
        PyObject *o;
        o = PyString_FromStringAndSize(arg3, arg5);
        resultobj = t_output_helper(resultobj,o);
        
        
        
        free(arg3);
        
    }
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chm_enumerate(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmFile *arg1 = (struct chmFile *) 0 ;
    int arg2 ;
    CHM_ENUMERATOR arg3 = (CHM_ENUMERATOR) 0 ;
    void *arg4 = (void *) 0 ;
    int result;
    PyObject * obj0 = 0 ;
    PyObject * obj2 = 0 ;
    PyObject * obj3 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"OiOO:chm_enumerate",&obj0,&arg2,&obj2,&obj3)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmFile,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    {
        if (!my_set_callback(self, obj2)) goto fail;
        arg3 = dummy_enumerator;
    }
    {
        if (!(arg4 = PyCObject_FromVoidPtr(obj3, NULL))) goto fail;
    }
    result = (int)chm_enumerate(arg1,arg2,arg3,arg4);
    
    resultobj = PyInt_FromLong((long)result);
    return resultobj;
    fail:
    return NULL;
}


static PyObject *_wrap_chm_enumerate_dir(PyObject *self, PyObject *args) {
    PyObject *resultobj;
    struct chmFile *arg1 = (struct chmFile *) 0 ;
    char *arg2 ;
    int arg3 ;
    CHM_ENUMERATOR arg4 = (CHM_ENUMERATOR) 0 ;
    void *arg5 = (void *) 0 ;
    int result;
    PyObject * obj0 = 0 ;
    PyObject * obj3 = 0 ;
    PyObject * obj4 = 0 ;
    
    if(!PyArg_ParseTuple(args,(char *)"OsiOO:chm_enumerate_dir",&obj0,&arg2,&arg3,&obj3,&obj4)) goto fail;
    if ((SWIG_ConvertPtr(obj0,(void **) &arg1, SWIGTYPE_p_chmFile,SWIG_POINTER_EXCEPTION | 0 )) == -1) SWIG_fail;
    {
        if (!my_set_callback(self, obj3)) goto fail;
        arg4 = dummy_enumerator;
    }
    {
        if (!(arg5 = PyCObject_FromVoidPtr(obj4, NULL))) goto fail;
    }
    result = (int)chm_enumerate_dir(arg1,(char const *)arg2,arg3,arg4,arg5);
    
    resultobj = PyInt_FromLong((long)result);
    return resultobj;
    fail:
    return NULL;
}


static PyMethodDef SwigMethods[] = {
	 { (char *)"chmUnitInfo_start_set", _wrap_chmUnitInfo_start_set, METH_VARARGS },
	 { (char *)"chmUnitInfo_start_get", _wrap_chmUnitInfo_start_get, METH_VARARGS },
	 { (char *)"chmUnitInfo_length_set", _wrap_chmUnitInfo_length_set, METH_VARARGS },
	 { (char *)"chmUnitInfo_length_get", _wrap_chmUnitInfo_length_get, METH_VARARGS },
	 { (char *)"chmUnitInfo_space_set", _wrap_chmUnitInfo_space_set, METH_VARARGS },
	 { (char *)"chmUnitInfo_space_get", _wrap_chmUnitInfo_space_get, METH_VARARGS },
	 { (char *)"chmUnitInfo_path_set", _wrap_chmUnitInfo_path_set, METH_VARARGS },
	 { (char *)"chmUnitInfo_path_get", _wrap_chmUnitInfo_path_get, METH_VARARGS },
	 { (char *)"new_chmUnitInfo", _wrap_new_chmUnitInfo, METH_VARARGS },
	 { (char *)"delete_chmUnitInfo", _wrap_delete_chmUnitInfo, METH_VARARGS },
	 { (char *)"chmUnitInfo_swigregister", chmUnitInfo_swigregister, METH_VARARGS },
	 { (char *)"chm_open", _wrap_chm_open, METH_VARARGS },
	 { (char *)"chm_close", _wrap_chm_close, METH_VARARGS },
	 { (char *)"chm_set_param", _wrap_chm_set_param, METH_VARARGS },
	 { (char *)"chm_resolve_object", _wrap_chm_resolve_object, METH_VARARGS },
	 { (char *)"chm_retrieve_object", _wrap_chm_retrieve_object, METH_VARARGS },
	 { (char *)"chm_enumerate", _wrap_chm_enumerate, METH_VARARGS },
	 { (char *)"chm_enumerate_dir", _wrap_chm_enumerate_dir, METH_VARARGS },
	 { NULL, NULL }
};


/* -------- TYPE CONVERSION AND EQUIVALENCE RULES (BEGIN) -------- */

static swig_type_info _swigt__p_chmUnitInfo[] = {{"_p_chmUnitInfo", 0, "struct chmUnitInfo *", 0},{"_p_chmUnitInfo"},{0}};
static swig_type_info _swigt__p_unsigned_char[] = {{"_p_unsigned_char", 0, "unsigned char *", 0},{"_p_unsigned_char"},{0}};
static swig_type_info _swigt__p_char[] = {{"_p_char", 0, "char *", 0},{"_p_char"},{0}};
static swig_type_info _swigt__CHM_ENUMERATOR[] = {{"_CHM_ENUMERATOR", 0, "CHM_ENUMERATOR", 0},{"_CHM_ENUMERATOR"},{0}};
static swig_type_info _swigt__p_chmFile[] = {{"_p_chmFile", 0, "struct chmFile *", 0},{"_p_chmFile"},{0}};

static swig_type_info *swig_types_initial[] = {
_swigt__p_chmUnitInfo, 
_swigt__p_unsigned_char, 
_swigt__p_char, 
_swigt__CHM_ENUMERATOR, 
_swigt__p_chmFile, 
0
};


/* -------- TYPE CONVERSION AND EQUIVALENCE RULES (END) -------- */

static swig_const_info swig_const_table[] = {
{ SWIG_PY_INT,     (char *)"CHM_UNCOMPRESSED", (long) (0), 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_COMPRESSED", (long) (1), 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_MAX_PATHLEN", (long) 256, 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_PARAM_MAX_BLOCKS_CACHED", (long) 0, 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_RESOLVE_SUCCESS", (long) (0), 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_RESOLVE_FAILURE", (long) (1), 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_ENUMERATE_NORMAL", (long) (1), 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_ENUMERATE_META", (long) (2), 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_ENUMERATE_SPECIAL", (long) (4), 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_ENUMERATE_FILES", (long) (8), 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_ENUMERATE_DIRS", (long) (16), 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_ENUMERATE_ALL", (long) (31), 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_ENUMERATOR_FAILURE", (long) (0), 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_ENUMERATOR_CONTINUE", (long) (1), 0, 0, 0},
{ SWIG_PY_INT,     (char *)"CHM_ENUMERATOR_SUCCESS", (long) (2), 0, 0, 0},
{0}};

#ifdef __cplusplus
}
#endif

#ifdef __cplusplus
extern "C"
#endif
SWIGEXPORT(void) SWIG_init(void) {
    static PyObject *SWIG_globals = 0; 
    static int       typeinit = 0;
    PyObject *m, *d;
    int       i;
    if (!SWIG_globals) SWIG_globals = SWIG_newvarlink();
    m = Py_InitModule((char *) SWIG_name, SwigMethods);
    d = PyModule_GetDict(m);
    
    if (!typeinit) {
        for (i = 0; swig_types_initial[i]; i++) {
            swig_types[i] = SWIG_TypeRegister(swig_types_initial[i]);
        }
        typeinit = 1;
    }
    SWIG_InstallConstants(d,swig_const_table);
    
}

