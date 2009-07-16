/**
 * Copyright (C) 2009 Joao Paulo de Souza Medeiros.
 *
 * Author(s): Joao Paulo de Souza Medeiros <ignotus21@gmail.com>
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
 */

#include <Python.h>

#include "bind/matrix.h"

void
delete(struct matrix *a)
{
    matrix_finalize(a);
    free((void *) a);
}

PyObject*
new(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    unsigned int rows, cols;

    if (!PyArg_ParseTuple(args, "II", &rows, &cols))
        return NULL;

    /**
     * Call the function
     */
    struct matrix *a =(struct matrix *) malloc(sizeof(struct matrix));

    matrix_initialize(a, rows, cols);

    /**
     * Convert output
     */
    return PyCObject_FromVoidPtr(a, (void *) delete);
}

PyObject*
get(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    unsigned int row, col;
    PyObject *m = NULL;

    if (!PyArg_ParseTuple(args, "OII", &m, &row, &col))
        return NULL;

    /**
     * Call the function
     */
    struct matrix *a = PyCObject_AsVoidPtr(m);

    if (row >= a->rows || col >= a->cols)
    {
        PyErr_SetString(PyExc_IndexError, "indexes exceed matrix size");
        return NULL;
    }

    /**
     * Convert output
     */
    return Py_BuildValue("d", (double) *matrix_value(a, row, col));
}

PyObject*
set(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    unsigned int row, col;
    PyObject *m = NULL;
    double value;

    if (!PyArg_ParseTuple(args, "OIId", &m, &row, &col, &value))
        return NULL;

    /**
     * Call the function
     */
    struct matrix *a = PyCObject_AsVoidPtr(m);

    if (row >= a->rows || col >= a->cols)
    {
        PyErr_SetString(PyExc_IndexError, "indexes exceed matrix size");
        return NULL;
    }

    *matrix_value(a, row, col) = (clann_type) value;

    /**
     * Convert output
     */
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject*
fill(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    PyObject *m = NULL;
    double value;

    if (!PyArg_ParseTuple(args, "Od", &m, &value))
        return NULL;

    /**
     * Call the function
     */
    struct matrix *a = PyCObject_AsVoidPtr(m);

    matrix_fill(a, (clann_type) value);

    /**
     * Convert output
     */
    Py_INCREF(Py_None);
    return Py_None;
}

PyObject*
identity(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    unsigned int n;

    if (!PyArg_ParseTuple(args, "I", &n))
        return NULL;

    /**
     * Call the function
     */
    struct matrix *a =(struct matrix *) malloc(sizeof(struct matrix));

    matrix_identity(a, n);

    /**
     * Convert output
     */
    return PyCObject_FromVoidPtr(a, (void *) delete);
}

PyObject*
transpose(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    PyObject *m = NULL;

    if (!PyArg_ParseTuple(args, "O", &m))
        return NULL;

    /**
     * Call the function
     */
    struct matrix *a =(struct matrix *) malloc(sizeof(struct matrix));

    matrix_transpose(PyCObject_AsVoidPtr(m), a);

    /**
     * Convert output
     */
    return PyCObject_FromVoidPtr(a, (void *) delete);
}

PyObject*
product(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    PyObject *a = NULL;
    PyObject *b = NULL;

    if (!PyArg_ParseTuple(args, "OO", &a, &b))
        return NULL;

    /**
     * Call the function
     */
    struct matrix *p =(struct matrix *) malloc(sizeof(struct matrix));

    matrix_product(PyCObject_AsVoidPtr(a), PyCObject_AsVoidPtr(b), p);

    /**
     * Convert output
     */
    return PyCObject_FromVoidPtr(p, (void *) delete);
}

PyObject*
inverse(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    PyObject *m = NULL;

    if (!PyArg_ParseTuple(args, "O", &m))
        return NULL;

    /**
     * Call the function
     */
    struct matrix *a =(struct matrix *) malloc(sizeof(struct matrix));

    if (!matrix_inverse(PyCObject_AsVoidPtr(m), a))
    {
        PyErr_SetString(PyExc_TypeError, "matrix does not have inverse");
        return NULL;
    }

    /**
     * Convert output
     */
    return PyCObject_FromVoidPtr(a, (void *) delete);
}

PyObject*
pseudo_inverse(PyObject *self, PyObject *args)
{
    /**
     * Convert input
     */
    PyObject *m = NULL;

    if (!PyArg_ParseTuple(args, "O", &m))
        return NULL;

    /**
     * Call the function
     */
    struct matrix *a =(struct matrix *) malloc(sizeof(struct matrix));

    if (!matrix_pseudo_inverse(PyCObject_AsVoidPtr(m), a))
    {
        PyErr_SetString(PyExc_TypeError,
                        "matrix does not have pseudo inverse");
        return NULL;
    }

    /**
     * Convert output
     */
    return PyCObject_FromVoidPtr(a, (void *) delete);
}

PyMODINIT_FUNC
initmatrix(void)
{
    PyObject *m;

    m = Py_InitModule4("matrix",
            MatrixMethods,
            module__doc__,
            (PyObject *)NULL,
            PYTHON_API_VERSION);

    if (m == NULL)
        return;

    MatrixError = PyErr_NewException("matrix.error", NULL, NULL);
    Py_INCREF(MatrixError);
    PyModule_AddObject(m, "error", MatrixError);

    if (PyErr_Occurred())
        Py_FatalError("can't initialize module matrix");
}