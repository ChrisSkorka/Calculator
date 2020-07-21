from Classes.built_ins import built_ins
from Classes.data_structures import *
from Classes.data_types import *



# Unary Operations: -, +
built_ins.register_left_unary_operator('+', 7)
built_ins.register_left_unary_operator('-', 7)

# Binary Operations:

# arithmetic
built_ins.register_binary_operator('+',   3)
built_ins.register_binary_operator('-',   3)
built_ins.register_binary_operator('*',   4)
built_ins.register_binary_operator('4',   4)
built_ins.register_binary_operator('/',   4)
built_ins.register_binary_operator('//',  4)
built_ins.register_binary_operator('%',   4)
built_ins.register_binary_operator('mod', 4)
built_ins.register_binary_operator('^',   5)

# matrix
built_ins.register_binary_operator('#',   4)
built_ins.register_binary_operator('matmul', 4)

# vector
built_ins.register_binary_operator('.*' , 4)
built_ins.register_binary_operator('dot', 4)

# root
built_ins.register_left_unary_operator('$', 6)
built_ins.register_binary_operator('$', 6)

# function call
built_ins.register_binary_operator('9', 9)
built_ins.set_evaluation_parameter('9', 1, 'force_array', True)

# function definition
built_ins.register_binary_operator('=>', 1)
built_ins.set_evaluation_parameter('=>', 0, 'references', True)
built_ins.set_evaluation_parameter('=>', 1, 'evaluable', True)

built_ins.register_binary_operator('=', 0)
built_ins.set_evaluation_parameter('=', 0, 'references', True)

# conversion
built_ins.register_binary_operator('@', -1)