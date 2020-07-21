from Classes.built_ins import built_ins
from Classes.data_types import *



def km_forwards(km):
    return Real(km.value * Decimal(1000))

def km_backwards(m):
    return Real(m.value / Decimal(1000))

def  m_forwards(m):
    return Real(m.value)

def  m_backwards(m):
    return Real(m.value)

def cm_forwards(cm):
    return Real(cm.value / Decimal(100))

def cm_backwards(m):
    return Real(m.value * Decimal(100))

def mm_forwards(mm):
    return Real(mm.value / Decimal(1000))

def mm_backwards(m):
    return Real(m.value * Decimal(1000))

def um_forwards(um):
    return Real(um.value / Decimal(1000000))

def um_backwards(m):
    return Real(m.value * Decimal(1000000))

def nm_forwards(nm):
    return Real(nm.value / Decimal(1000000000))

def nm_backwards(m):
    return Real(m.value * Decimal(1000000000))

def pm_forwards(pm):
    return Real(pm.value / Decimal(1000000000000))

def pm_backwards(m):
    return Real(m.value * Decimal(1000000000000))

built_ins.register_conversion_function_set('km', km_forwards, km_backwards)
built_ins.register_conversion_function_set( 'm',  m_forwards,  m_backwards)
built_ins.register_conversion_function_set('cm', cm_forwards, cm_backwards)
built_ins.register_conversion_function_set('mm', mm_forwards, mm_backwards)
built_ins.register_conversion_function_set('um', um_forwards, um_backwards)
built_ins.register_conversion_function_set('nm', nm_forwards, nm_backwards)
built_ins.register_conversion_function_set('pm', pm_forwards, pm_backwards)