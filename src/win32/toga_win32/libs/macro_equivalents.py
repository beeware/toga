#Some macro equivalents that are used all over in the windows API, namely LOWORD and HIWORD.
#macros are upper-case to match C/MSDN.

def LOWORD(word):
    return word & 0x0000FFFF

def HIWORD(word):
    return word & 0xffff0000
