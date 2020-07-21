from Classes.built_ins import built_ins
from Classes.data_types import *



def km3_forwards(km):
    return Real(km.value * Decimal(1000**3))

def km3_backwards(m):
    return Real(m.value / Decimal(1000**3))

def  m3_forwards(m):
    return Real(m.value)

def  m3_backwards(m):
    return Real(m.value)

def   l_forwards(l):
    return Real(l.value / Decimal(10**3))

def   l_backwards(m):
    return Real(m.value * Decimal(10**3))

def cm3_forwards(cm):
    return Real(cm.value / Decimal(100**3))

def cm3_backwards(m):
    return Real(m.value * Decimal(100**3))

def mm3_forwards(mm):
    return Real(mm.value / Decimal(1000**3))

def mm3_backwards(m):
    return Real(m.value * Decimal(1000**3))

def um3_forwards(um):
    return Real(um.value / Decimal(1000000**3))

def um3_backwards(m):
    return Real(m.value * Decimal(1000000**3))

def nm3_forwards(nm):
    return Real(nm.value / Decimal(1000000000**3))

def nm3_backwards(m):
    return Real(m.value * Decimal(1000000000**3))

def pm3_forwards(pm):
    return Real(pm.value / Decimal(1000000000000**3))

def pm3_backwards(m):
    return Real(m.value * Decimal(1000000000000**3))

built_ins.register_conversion_function_set('km3', km3_forwards, km3_backwards)
built_ins.register_conversion_function_set( 'm3',  m3_forwards,  m3_backwards)
built_ins.register_conversion_function_set(  'l',   l_forwards,   l_backwards)
built_ins.register_conversion_function_set('cm3', cm3_forwards, cm3_backwards)
built_ins.register_conversion_function_set( 'ml', cm3_forwards, cm3_backwards)
built_ins.register_conversion_function_set('mm3', mm3_forwards, mm3_backwards)
built_ins.register_conversion_function_set('um3', um3_forwards, um3_backwards)
built_ins.register_conversion_function_set('nm3', nm3_forwards, nm3_backwards)
built_ins.register_conversion_function_set('pm3', pm3_forwards, pm3_backwards)