import math, pyperclip, os

# os.system("mode con cols=65 lines=25")
# from ctypes import windll, byref, wintypes
# from ctypes.wintypes import SMALL_RECT

# # resize window
# STDOUT = -11
# hdl = windll.kernel32.GetStdHandle(STDOUT)
# rect = wintypes.SMALL_RECT(0, 50, 50, 80) # (left, top, right, bottom)
# windll.kernel32.SetConsoleWindowInfo(hdl, True, byref(rect))

# documentation
def help():
    print("""
OPERATION:    enter commands or expressions

COMMANDS:     perform fuctions such as configuration changes
    help:       this
    ref:        list of operations, functions and configurations
    copy:       OR '=' copys last result to clipboard
    clear:      clears screen
    exit:       exists application

    setdeg      sets default angle converson to degrees
    setrad      sets default angle converson to radians
    setgrad     sets default angle converson to grad

    setbin      sets output to binary (int)
    setoct      sets output to octal (int)
    setdec      sets output to decimal with format
    sethex      sets output to hexadecimal
    setpy       sets output to plain python representation

EXPRESSIONS:  perform calculations or assign vairable values
    equation:   equation to evaluate        eg: > 1 + ln(8)
    variables:  set var using '='           eg: > x = equation
                set var to last result      eg: > = x     -> x = ans
                use var in equations        eg: > 5 * x
    ans:        ans holds last result       eg: > 3 * ans
                continue with result        eg: > + 3     -> ans + 3
                copy last result            eg: > copy
                                            eg: > =

INPUT CONVERSION: use different input conversions
    angle:      use deg, rad or grad as c   eg: > sin(pi, rad)
    base:       use 0b, 0o or 0x            eg: > 0xA7 & 0b00010110

OPTIONAL PARAMETERS: some functions have optional parameters
    referece:   [...] is optional           eg: > log(9) + log(9, 3)
                [, c] in trig functions is
                is the angle converter

""")

# reference
def ref():
    print(
"""Python text based calculator (ref)

Commands and Configurations:   | Conversion:     | Vars:
Commands | Angles   | Output   | Base  | Angle c | Vars
help       setdeg     setbin   | 0b...   deg     | pi
ref        setrad     setoct   | 0o...   rad     | e
copy, =    setgrad    setdec   | 0x...   grad    | ans
clear                 sethex   |                 | var = expression
exit                  setpy    |                 |

Operators | Bitwise | Power & Log     | Trig         | Hyperbolic
**          ~         sqrt (x)          sin (x[, c])   sinh (x[, c])
*           <<        root (x[, exp])   cos (x[, c])   cosh (x[, c])
/           >>        exp  (x, exp)     tan (x[, c])   tanh (x[, c])
//          &         ln   (x)          asin(x[, c])   asinh(x[, c])
%           ^         log  (x[, b])     acos(x[, c])   acosh(x[, c])
+           |         log10(x)          atan(x[, c])   atanh(x[, c])
-                     log2 (x) 
fact(x)
""")

def clear():
    os.system("CLS")

ref()

# constants
deg = math.pi / 180
rad = 1
grad = math.pi / 200
pi = math.pi
e = math.e

# output base changer
def outDec(x): 
    l = str(round(x, 14)).split('.'); 
    d = l[0]
    d = ' ' * ( (3 - len(d) % 3) % 3) + d
    l[0] = ",".join([d[i:i+3] for i in range(0, len(d), 3)])
    return ".".join(l).strip()
def outBin(x): return bin(int(x))
def outOct(x): return oct(int(x))
def outHex(x): return hex(int(x))
def outPy(x):  return str(x)

# configuration setters
def setDeg():  global _angle; _angle = deg; return 0
def setRad():  global _angle; _angle = rad; return 0
def setGrad(): global _angle; _angle = grad; return 0

def setBin():  global _output; _output = outBin; return 0
def setOct():  global _output; _output = outOct; return 0
def setDec():  global _output; _output = outDec; return 0
def setHex():  global _output; _output = outHex; return 0
def setPy():   global _output; _output = outPy; return 0

# configurations
_angle = deg
_output = outDec

# function definitions
def sqrt(x):            return math.sqrt(x)
def root(x, exp=2):     return math.pow(x, 1/exp)
def exp(x, exp):        return math.pow(x, exp)
def log(x, b=10):       return math.log(x, b)
def log10(x):           return math.log(x, 10)
def log2(x):            return math.log(x, 2)
def ln(x):              return math.log(x, e)
def fact(x):            return math.factorial(x)
def sin(x, c=0):        return math.sin(x * (_angle if c == 0 else c))
def cos(x, c=0):        return math.cos(x * (_angle if c == 0 else c))
def tan(x, c=0):        return math.tan(x * (_angle if c == 0 else c))
def asin(x, c=0):       return math.asin(x) / (_angle if c == 0 else c)
def acos(x, c=0):       return math.acos(x) / (_angle if c == 0 else c)
def atan(x, c=0):       return math.atan(x) / (_angle if c == 0 else c)
def sinh(x, c=0):       return math.sinh(x * (_angle if c == 0 else c))
def cosh(x, c=0):       return math.cosh(x * (_angle if c == 0 else c))
def tanh(x, c=0):       return math.tanh(x * (_angle if c == 0 else c))
def asinh(x, c=0):      return math.asinh(x) / (_angle if c == 0 else c)
def acosh(x, c=0):      return math.acosh(x) / (_angle if c == 0 else c)
def atanh(x, c=0):      return math.atanh(x) / (_angle if c == 0 else c)

# controlled sandboxed environment for exec
virtualEnvironment = {
    '__builtins__': {},
    'ans':      0,
    'pi':       pi,
    'e':        e,
    'deg':      deg,
    'rad':      rad,
    'grad':     grad,
    '_angle':   deg,

    # functions
    'sqrt':     sqrt,
    'root':     root,
    'exp':      exp,
    'log':      log,
    'log10':    log10,
    'log2':     log2,
    'ln':       ln,
    'fact':     fact,
    'sin':      sin,
    'cos':      cos,
    'tan':      tan,
    'asin':     asin,
    'acos':     acos,
    'atan':     atan,
    'sinh':     sinh,
    'cosh':     cosh,
    'tanh':     tanh,
    'asinh':    asinh,
    'acosh':    acosh,
    'atanh':    atanh,
}

# evaluation cycle
while True:
    try:
        query = input("> ").strip()

        # commands
        if   query == 'exit':   break
        elif query == 'help':   help()
        elif query == 'ref':    ref()
        elif query == 'clear':  clear()
        elif query == 'copy':   pyperclip.copy(ans)
        elif query == '=':      pyperclip.copy(ans)
        elif query == 'setdeg': setDeg()
        elif query == 'setrad': setRad()
        elif query == 'setgrad':setGrad()
        elif query == 'setbin': setBin()
        elif query == 'setoct': setOct()
        elif query == 'setdec': setDec()
        elif query == 'sethex': setHex()
        elif query == 'setpy':  setPy()

        # evaluate query
        elif query != "":

            # = var           ->   saves ans into var
            if query[0] == '=':
                query = query[1:] + "=ans"
            
            # op expression   ->   ans op expression
            elif query[0] in "*/%+-<>&^|":
                query = "ans" + query

            # run query
            # exec("ans=" + query, virtualEnvironment, virtualEnvironment)
            exec("ans=" + query)

            # print formated and processed results
            # print("  =", _output(virtualEnvironment['ans']))
            print("  =", _output(ans))
            print("")

    # catch and display all errors
    except Exception as e:
        print("Error:", e)
        print("")