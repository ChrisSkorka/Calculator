from Classes.built_ins import built_ins
from Classes.data_types import *



def km2_forwards(km):
    return Real(km.value * Decimal(1000**2))

def km2_backwards(m):
    return Real(m.value / Decimal(1000**2))

def  m2_forwards(m):
    return Real(m.value)

def  m2_backwards(m):
    return Real(m.value)

def cm2_forwards(cm):
    return Real(cm.value / Decimal(100**2))

def cm2_backwards(m):
    return Real(m.value * Decimal(100**2))

def mm2_forwards(mm):
    return Real(mm.value / Decimal(1000**2))

def mm2_backwards(m):
    return Real(m.value * Decimal(1000**2))

def um2_forwards(um):
    return Real(um.value / Decimal(1000000**2))

def um2_backwards(m):
    return Real(m.value * Decimal(1000000**2))

def nm2_forwards(nm):
    return Real(nm.value / Decimal(1000000000**2))

def nm2_backwards(m):
    return Real(m.value * Decimal(1000000000**2))

def pm2_forwards(pm):
    return Real(pm.value / Decimal(1000000000000**2))

def pm2_backwards(m):
    return Real(m.value * Decimal(1000000000000**2))

built_ins.register_conversion_function_set('km2', km2_forwards, km2_backwards)
built_ins.register_conversion_function_set( 'm2',  m2_forwards,  m2_backwards)
built_ins.register_conversion_function_set('cm2', cm2_forwards, cm2_backwards)
built_ins.register_conversion_function_set('mm2', mm2_forwards, mm2_backwards)
built_ins.register_conversion_function_set('um2', um2_forwards, um2_backwards)
built_ins.register_conversion_function_set('nm2', nm2_forwards, nm2_backwards)
built_ins.register_conversion_function_set('pm2', pm2_forwards, pm2_backwards)