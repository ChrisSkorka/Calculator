from Classes.built_ins import built_ins
from Classes.data_types import *



def  ms_forwards(ms):
    return Real(ms.value / Decimal(1000))

def  ms_backwards(s):
    return Real(s.value * Decimal(1000))

def   s_forwards(s):
    return Real(s.value)

def   s_backwards(s):
    return Real(s.value)

def min_forwards(min):
    return Real(min.value * Decimal(60))

def min_backwards(s):
    return Real(s.value / Decimal(60))

def  hr_forwards(hr):
    return Real(hr.value * Decimal(3600))

def  hr_backwards(s):
    return Real(s.value / Decimal(3600))

def day_forwards(day):
    return Real(day.value * Decimal(86400))

def day_backwards(s):
    return Real(s.value / Decimal(86400))

def time_forwards(string):
    pattern = r'(?:(\d+)(?:d|D)\s*)?(\d{1,2})(?:h|H)?:(\d{1,2})(?:m|M)?(?::(\d{1,2}(?:\.\d+)?)(?:s|S)?)?'
    match = re.fullmatch(pattern, string.value.strip())
    if match:
        d = match.group(1) or 0
        h = match.group(2) or 0
        m = match.group(3) or 0
        s = match.group(4) or 0
        return Tensor(Real( Decimal(d) * 86400 + Decimal(h) * 3600 + Decimal(m) * 60 + Decimal(s)))
    else:
        raise Exception(f'Invalid time formatting: "{string.value}"')

def time_backwards(t):
    t = t.value
    d = t // Decimal(86400)
    t -= d * Decimal(86400)
    h = t // Decimal(3600)
    t -= h * Decimal(3600)
    m = t // Decimal(60)
    t -= m * Decimal(60)
    s = t // Decimal(1)
    t -= s * Decimal(1)
    ms = t // Decimal('0.001')
    t -= ms * Decimal('0.001')
    ps = t / Decimal('0.000001')
    
    str_d = str(int(d))
    str_h = str(int(h)).zfill(2)
    str_m = str(int(m)).zfill(2)
    str_s = str(int(s)).zfill(2)
    str_ms = str(int(ms)).zfill(3)
    str_ps = str(int(ps)).zfill(3)
    
    str_days = '' if d == 0 else                    f'{str_d}d ' 
    str_time =                                      f'{str_h}h:{str_m}m:{str_s}'
    str_fraction_1 = '' if ms == 0 and ps == 0 else f'.{str_ms}'
    str_fraction_2 = '' if ps == 0 else             f'{str_ps}'
    
    return Tensor(String( str_days+str_time+str_fraction_1+str_fraction_2+'s' ))
        

built_ins.register_conversion_function_set(  'ms',   ms_forwards,   ms_backwards)
built_ins.register_conversion_function_set(   's',    s_forwards,    s_backwards)
built_ins.register_conversion_function_set( 'min',  min_forwards,  min_backwards)
built_ins.register_conversion_function_set(  'hr',   hr_forwards,   hr_backwards)
built_ins.register_conversion_function_set( 'day',  day_forwards,  day_backwards)
built_ins.register_conversion_function_set('time', time_forwards, time_backwards)