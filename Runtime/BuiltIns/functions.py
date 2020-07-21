from Classes.built_ins import built_ins
from Classes.data_structures import *
from Classes.data_types import *



# Assignment: =
def assignment(environment, key, value):
    
    if type(key) == Array:
        for k, v in zip(key, value):
            assignment(environment, k, v)
    else:
        environment[key.first.value] = value
        
    return value

built_ins.register_function('=', assignment, True, (Array, None))
built_ins.register_function('=', assignment, True, (Reference, None))



# Function Definition: =>
def define_function(environment, parameters, evaluable):
    
    if type(parameters) == Tensor and parameters.dtype == Reference:
        parameter_names = [parameters.first.value]
    elif type(parameters) == Array:
        parameter_names = [p.first.value for p in parameters.data]
    
    parameter_types = tuple([None] * len(parameter_names))
    
    def function(environment):
        return evaluable.eval(environment)
    
    function_signature = FunctionSignature('', function, parameter_names, parameter_types, parameter_ranks=None, parameter_shapes=None)

    function_set = FunctionSet('')
    function_set.add(function_signature)
    
    return function_set

built_ins.register_function('=>', define_function, True, (Reference, None))
built_ins.register_function('=>', define_function, True, (Array, None))



# Unary Operations: -, +
built_ins.register_function('+', lambda t:Tensor(Real(+t.first.value)), None, (Real,), (0,))
built_ins.register_function('-', lambda t:Tensor(Real(-t.first.value)), None, (Real,), (0,))



# Binary Operantors: +, -, *, /, //, %, ^
# A + B
built_ins.register_function('+', lambda a, b: Tensor(Real(a.first.value + b.first.value)), None, (Real, Real), (0, 0))

# A - B
built_ins.register_function('-', lambda a, b: Tensor(Real(a.first.value - b.first.value)), None, (Real, Real), (0, 0))

# A * B
built_ins.register_function('*', lambda a, b: Tensor(Real(a.first.value * b.first.value)), None, (Real, Real), (0, 0))
# built_ins.register_function('9', lambda a, b: Tensor(Real(a.first.value * b.first.value)), None, (Real, Real), (0, 0))

# A / B
built_ins.register_function('/', lambda a, b: Tensor(Real(a.first.value / b.first.value)), None, (Real, Real), (0, 0))

# A // B
built_ins.register_function('//', lambda a, b: Tensor(Real(a.first.value // b.first.value)), None, (Real, Real), (0, 0))

# A % B
built_ins.register_function('%', lambda a, b: Tensor(Real(a.first.value % b.first.value)), None, (Real, Real), (0, 0))
built_ins.register_function('mod', lambda a, b: Tensor(Real(a.first.value % b.first.value)), None, (Real, Real), (0, 0))

# A ^ B
built_ins.register_function('^', lambda a, b: Tensor(Real(a.first.value ** b.first.value)), None, (Real, Real), (0, 0))



# Matrix Multiplication: #
def matmul(A, B):
    
    a_shape = A.shape
    b_shape = B.shape
    
    assert A.rank >= 2 and B.rank >= 2, 'left and right sides must be matrices'
    assert a_shape[-1] == b_shape[-2], 'left n_cols must equal right n_rows'
    
    n_rows = a_shape[0]
    n_cols = b_shape[1]
    n_vec = a_shape[1]
    shape = (n_rows , n_cols)
    
    data = np.empty(shape, dtype=object)
    
    for row in range(n_rows):
        for col in range(n_cols):
            v = 0
            for i in range(n_vec):
                v += A[(row, i)].first.value * B[(i, col)].first.value
            data[row,col] = Real(v)
    
    return Tensor(data, shape)

built_ins.register_function('#', matmul, None, (Real, Real), (2, 2))
built_ins.register_function('matmul', matmul, None, (Real, Real), (2, 2))



# Vector Dot Product: .*
def dot(A, B):
    
    a_shape = A.shape
    b_shape = B.shape
    
    assert A.rank == 1 and B.rank == 1, 'left and right sides must be vectors'
    assert a_shape == b_shape, 'vector length must match'
    
    n_vec = a_shape[-1]
    
    v = 0
    for i in range(n_vec):
        v += A[(i,)].first.value * B[(i,)].first.value
    
    return Tensor(Real(v))

built_ins.register_function('.*', dot, None, (Real, Real), (1, 1))
built_ins.register_function('dot', dot, None, (Real, Real), (1, 1))



# Absolute value abs
def absolute(A):
    return Tensor(Real(abs(A.first.value)))

built_ins.register_function('abs', absolute, None, (Real,), (0,))



# Root and Square root $
def root(A, B):
    return Tensor(Real(B.first.value ** (Decimal(1) / A.first.value)))

def sqrt(A):
    return Tensor(Real(A.first.value ** Decimal(0.5)))

built_ins.register_function('$', sqrt, None, (Real,), (0,))
built_ins.register_function('$', root, None, (Real, Real), (0, 0))



# Function Call
def function_call(environment, function_set, parameters):
    return function_set.eval(environment, parameters)

built_ins.register_function('9', function_call, True, (FunctionSet, Array))


def foo(A):
    return Tensor(Real(A.first.value * A.first.value))
def bar(A, B):
    return Tensor(Real(A.first.value * B.first.value))
    
built_ins.register_function('fun', foo, False, (Real,), (0,))
built_ins.register_function('fun', bar, False, (Real, Real), (0, 0))



# Tensor Lookup
def tensor_lookup(environment, tensor, parameters):
    index = [int(p.first.value) for p in parameters]
    return tensor[tuple(index)]

built_ins.register_function('9', tensor_lookup, True, (Real, Array))



# Array Lookup
def array_lookup(environment, array, parameters):
    index = [int(p.first.value) for p in parameters]
    return array[tuple(index)]

built_ins.register_function('9', array_lookup, True, (Array, Array))



# Conversion @, [implocit]
def conversion_forwards_function_call(environment, tensor, conversion_function_set):
    return conversion_function_set.eval(environment, tensor, True)

def conversion_backwards_function_call(environment, tensor, conversion_function_set):
    return conversion_function_set.eval(environment, tensor, False)

built_ins.register_function('9', conversion_forwards_function_call, True, (None, ConversionFunctionSet))
built_ins.register_function('@', conversion_backwards_function_call, True, (None, ConversionFunctionSet))