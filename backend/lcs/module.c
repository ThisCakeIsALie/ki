#include <Python.h>
#include <stdio.h>

void to_list(PyObject* seq_obj, char** seq, size_t size) {
    PyObject* strObj;

    for (int i = 0; i < size; ++i) {
        strObj = PyTuple_GetItem(seq_obj, i);
        seq[i] = PyUnicode_AsUTF8(strObj);
    }
}

int calc_lcs_distance(char** seq1, char** seq2, size_t seq1_size, size_t seq2_size) {
    int i, j;
    int x = seq1_size + 1;
    int y = seq2_size + 1;

    int* cache = malloc(x * y * sizeof(int));

    for (i = 0; i < x; ++i) {
        cache[y * i] = 0;
    }

    for (i = 0; i < y; ++i) {
        cache[i] = 0;
    }

    for (i = 1; i < x; ++i) {
        for (j = 1; j < y; ++j) {
            if (strcmp(seq1[i-1], seq2[j-1]) == 0) {
                cache[y * i + j] = cache[y * (i - 1) + (j - 1)] + 1;
            } else {
                int first = cache[y * (i - 1) + j];
                int second = cache[y * i + (j - 1)];

                cache[y * i + j] = first > second ? first : second;
            }
        }
    }

    free(cache);

    return seq1_size + seq2_size - 2 * cache[y * seq1_size + seq2_size];
}

static PyObject* lcs_distance(PyObject* self, PyObject* args) {
    PyObject* seq1_obj;
    PyObject* seq2_obj;

    if (!PyArg_ParseTuple(args, "O!O!", &PyTuple_Type, &seq1_obj, &PyTuple_Type, &seq2_obj)) {
        return NULL;
    }

    size_t seq1_size = PyTuple_Size(seq1_obj);
    char** seq1 = malloc(seq1_size * sizeof(char*));

    size_t seq2_size = PyTuple_Size(seq2_obj);
    char** seq2 = malloc(seq2_size * sizeof(char*));

    to_list(seq1_obj, seq1, seq1_size);
    to_list(seq2_obj, seq2, seq2_size);

    int result = calc_lcs_distance(seq1, seq2, seq1_size, seq2_size);

    free(seq1);
    free(seq2);
    return Py_BuildValue("i", result);
}

static PyMethodDef func_table[] = {
    { "lcs_distance", lcs_distance, METH_VARARGS, "Calculates longest common subsequence distance" },
    { NULL, NULL, 0, NULL }
};

static struct PyModuleDef lcs = {
    PyModuleDef_HEAD_INIT,
    "lcs",
    "Module to calculate longest common subsequence distance",
    -1,
    func_table
};

PyMODINIT_FUNC PyInit_lcs(void) {
    return PyModule_Create(&lcs);
}