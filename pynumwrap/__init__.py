# -*- coding: utf-8 -*-
from six.moves import builtins
import cmath
try:
    import mpmath
except:
    pass
try:
    import numpy as np
except:
    pass
try:
    import sympy as sy
except:
    pass

##########################################################
####################### Constants ########################
##########################################################

mode_python = 0
mode_mpmath = 1
dps_default_python = 25
dps_default_mpmath = 100

##########################################################
####################### Variables ########################
##########################################################

mode = mode_python
dps = dps_default_python
pi = cmath.pi

##########################################################
################# Configuration Functions ################
##########################################################

def usePythonTypes(dpsNew=dps_default_python):
    global mode, dps, pi
    mode = mode_python
    dps = dpsNew
    pi = cmath.pi

def useMpmathTypes(dpsNew=dps_default_mpmath):
    global mode, dps, pi
    mode = mode_mpmath
    dps = dpsNew
    pi = mpmath.pi
    mpmath.mp.dps = dps

############### BASIC TYPES ###############

# For convenience:
class mpf(mpmath.mpf):
    pass

# np.percentile need these overrides.
class mpc(mpmath.mpc):
    def __lt__(self, other):
        return self.real < other.real
        
    def __le__(self, other):
        return self.real <= other.real
        
    def __gt__(self, other):
        return self.real > other.real
    
    def __ge__(self, other):
        return self.real >= other.real

def float(val):
    if mode == mode_python:
        return builtins.float(val)
    else:
        return mpmath.mpf(val)

def complex(val):
    if mode == mode_python:
        return builtins.complex(val)
    else:
        if type(val) is str or type(val) is unicode:
            if 'nan' in val:
                return mpmath.mpc(real='nan',imag='nan')
            real = None
            imag = None
            delim = None
            if '+' in val[1:]:
                delim = '+'
            elif '-' in val[1:]:
                delim = '-'
            if delim is None:
                if 'j' in val:
                    imag = val.replace('j','')
                else:
                    real = val
            else:
                index = val[1:].find(delim) + 1
                real = val[:index]
                imag = val[index:].replace('j','')
            return mpmath.mpc(real=real,imag=imag)
        else:
            return mpmath.mpc(val)

def toSympy(val):
    if mode == mode_python:
        return val
    else:
        return sy.Float(str(val.real),dps) + sy.Float(str(val.imag),dps)*sy.I

def tompmath(val):
    if mode == mode_python:
        return mpmath.mpc(val.real,val.imag)
    else:
        return mpmath.mpc(real=sy.re(val),imag=sy.im(val))

############### BASIC OPERATIONS ###############
def percentile(a, q, axis=None, out=None, overwrite_input=False,
               interpolation='linear', keepdims=False):
    # Currently don't support percentile for mp types. Just convert the type.
    if mode == mode_python:
        return np.percentile(a, q, axis, out, overwrite_input, interpolation,
                             keepdims)
    else:
        return np.percentile(map(lambda v: mpc(v), a), q, axis, out, 
                             overwrite_input, interpolation, keepdims)

def pow(x, y):
    if mode == mode_python:
        return builtins.pow(x, y)
    else:
        return mpmath.power(x, y)

def exp(x):
    if mode == mode_python:
        return cmath.exp(x)
    else:
        return mpmath.exp(x)

def sqrt(x):
    if mode == mode_python:
        return cmath.sqrt(x)
    else:
        return mpmath.sqrt(x)

def tan(x):
    if mode == mode_python:
        return cmath.tan(x)
    else:
        return mpmath.tan(x)

def polar(x):
    if mode == mode_python:
        return cmath.polar(x)
    else:
        return mpmath.polar(x)

def roots(coeff):
    # Currently don't support roots for mp types. Just convert the type.
    if mode == mode_python:
        return np.roots(coeff)
    else:
        mappedCoeff = map(lambda val: builtins.complex(val), coeff)
        return np.roots(mappedCoeff)

############### MATRIX TYPES ###############

def matrix(val):
    if mode == mode_python:
        return np.matrix(val, dtype=np.complex128)
    else:
        return mpmath.matrix(val)

def sqZeros(sz):
    if mode == mode_python:
        return np.matrix(np.zeros((sz, sz), dtype=np.complex128))
    else:
        return mpmath.zeros(sz)

def identity(sz):
    if mode == mode_python:
        return np.matrix(np.identity(sz, dtype=np.complex128))
    else:
        return mpmath.eye(sz)

############# MATRIX CHARACTERISTICS #############
    
def shape(mat):
    if mode == mode_python:
        return mat.shape
    else:
        return (mat.rows, mat.cols)

def size(mat):
    if mode == mode_python:
        return mat.size
    else:
        return mat.rows*mat.cols

############### MATRIX OPERATIONS ###############

def lin_solve(mat, vec, **kwargs):
    if mode == mode_python:
        return np.linalg.solve(mat, vec, **kwargs)
    else:
        return mpmath.qr_solve(mat, vec, **kwargs)[0]

def diagonalise(mat):
    if mode == mode_python:
        w, v = np.linalg.eig(mat)
        P = np.transpose(np.matrix(v, dtype=np.complex128))
        return np.dot(P, np.dot(mat, np.linalg.inv(P)))
    else:
        w, v = mpmath.eig(mat)
        P = mpmath.matrix(v).T
        return P * mat * P**-1

def invert(mat):
    if mode == mode_python:
        return np.linalg.inv(mat)
    else:
        return mpmath.inverse(mat)

def dot(matA, matB):
    if mode == mode_python:
        return np.dot(matA, matB)
    else:
        return matA * matB

def getRow(mat, m):
    if mode == mode_python:
        return mat[m].tolist()[0]
    else:
        row = []
        for n in range(mat.cols):
            row.append(mat[m,n])
        return row

def getVector(mat, m):
    if mode == mode_python:
        return np.array(mat[m].tolist()[0])
    else:
        row = []
        for n in range(mat.cols):
            row.append(mat[m,n])
        return mpmath.matrix(row)

def copyRow(src_mat, dest_mat, m):
    newMat = dest_mat.copy()
    if mode == mode_python:
        for n in range(newMat.shape[1]):
            newMat[m,n] = src_mat[m,n]
    else:
        for n in range(newMat.cols):
            newMat[m,n] = src_mat[m,n]
    return newMat

def det(mat):
    if mode == mode_python:
        return np.linalg.det(mat)
    else:
        return mpmath.det(mat)

def sumElements(mat):
    if mode == mode_python:
        XS = 0.0
        for x in np.nditer(mat, flags=['refs_ok']):
            XS += x
    else:
        XS = mpmath.mpc(0.0)
        for i in range(mat.rows):
            for j in range(mat.cols):
                XS += mat[i,j]
    return XS

def trace(mat):
    if mode == mode_python:
        return np.trace(mat)
    else:
        t = mpmath.mpc(0.0)
        for i in range(mat.rows):
            t += mat[i,i]
        return t

def atanElements(mat):
    if mode == mode_python:
        return np.arctan(mat)
    else:
        at = mpmath.matrix(mat.rows, mat.cols)
        for i in range(mat.rows):
            for j in range(mat.cols):
                at[i,j] = mpmath.atan(mat[i,j])
        return at

def _toSymMatrix(mat):
    if mode == mode_python:
        return sy.Matrix(mat)
    else:
        symMat = sy.zeros(mat.rows, mat.cols)
        for r in range(mat.rows):
            for c in range(mat.cols):
                symMat[r,c] = mat[r,c]
        return symMat

def _fromSympytompmathMatrix(mat):
    mpMat = mpmath.matrix(mat.shape[0])
    for r in range(mat.shape[0]):
        for c in range(mat.shape[0]):
            mpMat[r,c] = tompmath(mat[r,c])
    return mpMat

def adjugate(mat):
    symMat = _toSymMatrix(mat)
    return _fromSympytompmathMatrix(symMat.adjugate())

############### MATRIX COMPARISONS ###############

def areMatricesClose(mat1, mat2, rtol=1e-05, atol=1e-08, equal_nan=False):
    if mode == mode_python:
        return np.allclose(mat1, mat2, rtol, atol, equal_nan)
    else:
        if shape(mat1) != shape(mat2):
            return False
        for r in range(mat1.rows):
            for c in range(mat1.cols):
                a = mat1[r,c]
                b = mat2[r,c]
                if mpmath.isnan(a) and mpmath.isnan(b) and equal_nan:
                    pass
                elif not numCmp(a, b, atol, rtol):
                    return False
    return True

############### OTHER ###############

def formattedFloatString(val, dps):
    if mode == mode_python:
        return ("{:1."+str(dps)+"f}").format(val)
    else:
        return mpmath.nstr(val, mpIntDigits(val)+dps)

def formattedComplexString(val, dps):
    if val.imag < 0.0:
        signStr = ""
    else:
        signStr = "+"
    rstr = formattedFloatString(val.real, dps)
    istr = formattedFloatString(val.imag, dps)+"j"
    return rstr + signStr + istr

def floatList(lst):
    return str(map(lambda x:str(x),lst)).replace("'","")

def mpIntDigits(num):
    if not mpmath.almosteq(num,0):
        a = mpmath.log(abs(num), b=10)
        b = mpmath.nint(a)
        if mpmath.almosteq(a,b):
            return int(b)+1
        else:
            c = mpmath.ceil(a)
            try:
                return int(c)
            except:
                pass
    else:
        return 0

def numCmp(a, b, atol, rtol):
    return abs(a-b) <= atol + rtol * abs(b)
