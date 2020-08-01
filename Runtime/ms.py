#!/usr/bin/env python
# coding: utf-8

# # Imports

# In[1]:


import math, pyperclip, os, re
from decimal import Decimal
import numpy as np
from functools import reduce
from itertools import product
from datetime import datetime, date, time


# # Docs

# In[2]:


"""
Data types: Real, Complex, Int, Boolean, String, Undefined
Data structures: Scalar, Vector, Matrix, ...
Variables: v
Functions: fun
Named operators: v operation u
Conversion specifier: 45deg
Data properties: object.property
Oppertation: Numeric, Sets, Comparison 

Data Structures
Tensor: [a, b,, c, d,,, ...]
List: (a, b, c, ...)
Function Body: {expression}

Implicit Operations
2(expression)      *
(expression)2      *
var(expression)    *
fun(parameters)    call

Named operators
on two values: v operation u
on one value: v.operation

Input and Output conversion
1m + 12cm @ cm
2hr + 45min + 1hr + 30min @ datetime
0b1100 * 0xFF @ dec

Basic Operations:
Standard:       | Bitwise: int&bool | Comparison:           | 
+           add | ~             not | ==             equals | 
-      subtract | &&            and | !=          not equal | 
*      multiply | ||             or | <           less than | 
/        divide | <xor>         xor | >        greater then | 
//      int div | <<     left shift | <=      less or equal | 
%       modulus | >>    right shift | >=   greater or equal | 
^         power |                   |                       | 
!     factorial |                   |                       | 
|val|  absolute |                   |                       | 
=    assignment |                   |                       | 

Ternary Operators
= =                return values = function = body
a < x < b          between
a if cond else b   

Higher Ranking Data Structure Operations:
Vector:                 | Matrix:                          | Reductions:
<dot>       dot product | <matmul>   matrix multiplication | <all>
<cross>   cross product | |mat|                            | <any>
|vec|            length | .T              transpose matrix | <
.length          length | 
.angle            angle | 



1 + sqrt 4
1 + sqrt x
1 + $4
1 + 3 root 8
1 + b root x
1 + b $ x

10 nPr 2
n nPr r
10 nCr 2
n nCr r

[1, 2,, 3, 4] # [5, 6,, 7, 8]
[1, 2,, 3, 4].T
mat1.T

5*x

sin 30deg
sin pi
sin2 pi
sini 0.5

Function definitions
fun = x => x^2               single value output
fun = x => [x, x*2, x^2]     tensor outputs
fun = x => (x, x*2, x^2)     multiple outputs
fun = x => {                 piecewise function
    0,   if x < 0 ; 
    x^2, if 0 <= x <= 1 ; 
    x,   else
}
fun(x) = {                  piecewise function
    0   if x < 0
    x^2 if 0 <= x <= 1
    x   else
}

fun(x,y,z) = {
    a = x+2
    b = y*2
    c = z^2
    (a,b,c)
}

if x < 0 {
    x = 0
}

for i = 0:10{
    x += i
}

while x < 0 {
    x += 1
}

@display = scientific 8
@display = hex


Statistical Operations:
"""
None


# In[3]:


"""
Conversion specifiers

Time:
    Seconds: s, ms, µs, ns, ps, 
        fs, as, zs, ys, ks, Ms, Gs, Ts, Ps, Es, Zs, Ys
    Other: min, hr, D, W, M, Y, am, pm
    
Distance:
    Metric: m, dm, cm, mm, µm, nm, pm, km, 
        fm, am, zm, ym, Mm, Gm, Tm, Pm, Em, Zm, Ym
    Imperial: th, in, ft, yd, mi
    Other: nmi

Mass: 
    Metrix: mg, µg, ng, pg, kg, Mg, tonne
        dg, cg, fg, ag, zg, yg, dag, hg, Mg, Gg, Tg, Pg, Eg, Zg, Yg
    Imperial: oz, lb, ton
    Other: mol
    
Temparature: K, C, F, R

Luminosity: cd, lx

Force: N, kN, lbf, pdl

"""
None


# # Classes

# ## Exceptions

# ### TokenNotAllowedException

# In[4]:


class TokenNotAllowedException(Exception):
    def __init__(self, source, ln=None, offset=None):
        if ln == None and offset == None:
            ln = source.ln
            offset = source.offset
            source = source.source
            
        message = f"\n{source.getSourcePointerString(ln, offset)}"
        
        super().__init__(message)


# ### VariableNotDefined

# In[5]:


class VariableNotDefined(Exception):
    def __init__(self, name):
        super().__init__(f"'{name}'")


# ### NotImplementedException

# In[6]:


class NotImplementedException(Exception):
    pass


# ## Token Matching

# ### TokenOperandDefinition

# In[7]:


class TokenOperandDefinition():
    """Defines an operand token that can be matched with using a string search"""
    
    def __init__(self, token, precedence):
        """Arguments:
            str   token:       string that identifies the operand
            float precedence:  precedence in order of operations (higher is executed first)
        """
        
        self.token = token
        self.precedence = float(precedence)
        
    def __repr__(self):
        return str(self)
        
    def __str__(self):
        return f'TokenOperandDefinition({self.token}, {self.precedence})'


# ### TokenGroupDefinition

# In[8]:


class TokenGroupDefinition():
    """Defines an grouping token pair that can be matched with using a string search"""
    
    def __init__(self, open_token, close_token, seperators, ignore_missing, function):
        """Arguments:
            str      open_token:          string that identifies the opening token
            str      close_token:         string that identifies the closing token (can be the same as open_token)
            dict(str: depth) seperators:  allowed seperators and their seperating depth
            function function:            the function to convert the list of items into an in environment object
        """
        
        self.open_token = open_token
        self.close_token = close_token
        self.seperators = seperators
        self.ignore_missing = ignore_missing
        
        self.function = function
        
    def __repr__(self):
        return str(self)
        
    def __str__(self):
        return f'TokenGroupDefinition({self.open_token}, {self.close_token})'


# ### TokenNewItemDefinition

# In[9]:


class TokenNewItemDefinition():
    """Defines an item seperation token that can be matched with using a string search"""
    
    def __init__(self, token):
        """Arguments:
            str token:  string that identifies the seperator
        """
        
        self.token = token
        
    def __repr__(self):
        return str(self)
        
    def __str__(self):
        return f'TokenNewItemDefinition({self.token}, {self.levels})'


# ### Source

# In[10]:


class Source:
    
    def __init__(self, string=''):
        self.string = string
        self.lines = []
        
    def set(self, string):
        self.string = string
        self.lines = string.splitlines(True)
        
    def getSourcePointerString(self, ln, offset):
        ln_number_string = str(ln+1)
        line = f'{ln_number_string}: {self.lines[ln]}'
        pointer = ' ' * (len(ln_number_string) + 2 + offset) + '↑'
        sep = '' if '\n' in line[-2:] else '\n'
        
        return line + sep + pointer


# ### Token

# In[11]:


class Token:
    
    def __init__(self, token_type, string, ln, offset, source):
        self.token_type = token_type
        self.string     = string
        self.ln         = ln
        self.offset     = offset
        self.source     = source
        
    def getSourcePointerString(self):
        return self.source.getSourcePointerString(self.ln, self.offset)


# ## Token Tree Nodes

# ### Abstract NodeToken

# In[12]:


class NodeToken():
    """represents a value, operation or grouping node that returns an evaluabe that can be evaluated to return a value"""
    
    def is_complete(self):
        """Returns whether this token is complete, if false, it is not a valud token and interpreting failed"""
        
        raise NotImplementedException('NodeToken.is_complete()')
        
    def set_left(self, node):
        """sets the left child node if it exists"""
        
        raise NotImplementedException('NodeToken.set_left(node)')

    def set_right(self, node):
        """sets the right child node if it exists"""
        
        raise NotImplementedException('NodeToken.set_right(node)')
        
    def get_right(self):
        """segetsts the right child node if it exists"""
        
        raise NotImplementedException('NodeToken.get_right()')
        
    def get_evaluable(self):
        """return an Evaluable obejct from this token, the token should be complete before this method is called"""
        
        raise NotImplementedException('NodeToken.get_evaluable()')


# ### NodeBinary

# In[13]:


class NodeBinary(NodeToken):
    """represents a binary operation with a left and right child"""
    
    def __init__(self, operation_definition, parent=None):
        self.parent = parent
        self.operation_definition = operation_definition
        self.precedence = operation_definition.precedence
        self.left = None
        self.right = None
    
    def is_complete(self):
        return self.left != None and self.right != None and self.left.is_complete() and self.right.is_complete()
        
    def set_left(self, node):
        """sets left child"""
        
        self.left = node
        node.parent = self

    def set_right(self, node):
        """sets right child"""
        
        self.right = node
        node.parent = self
        
    def get_right(self):
        """returns right child"""
        
        return self.right
    
    def get_evaluable(self):
        """returns Evaluable that computes a result from both child tokens"""
        
        return VariableFunction(self.operation_definition.token, (self.left.get_evaluable(), self.right.get_evaluable()))
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'NodeBinary({self.operation_definition}, left={self.left}, right={self.right})'


# ### NodeUnaryLeft

# In[14]:


class NodeUnaryLeft(NodeToken):
    """represents a unary operator to the left of its operand with a single child"""
    
    def __init__(self, operation_definition, parent=None):
        self.parent = parent
        self.operation_definition = operation_definition
        self.precedence = operation_definition.precedence
        self.child = None
    
    def is_complete(self):
        return self.child != None and self.child.is_complete()
        
    def set_left(self, node):
        """sets single child"""
        
        self.child = node
        node.parent = self

    def set_right(self, node):
        """sets single child"""
        
        self.child = node
        node.parent = self
        
    def get_right(self):
        """gets single child"""
        
        return self.child
    
    def get_evaluable(self):
        """returns Evaluable that computes a result from the child token"""
        
        return VariableFunction(self.operation_definition.token, (self.child.get_evaluable(), ))
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'NodeUnaryLeft({self.operation_definition}, child={self.child})'


# ### NodeUnaryRight

# In[15]:


class NodeUnaryRight(NodeToken):
    """represents a unary operator to the right of its operand with a single child"""
    
    def __init__(self, operation_definition, parent=None):
        self.parent = parent
        self.operation_definition = operation_definition
        self.precedence = operation_definition.precedence
        self.child = None
    
    def is_complete(self):
        return self.child != None and self.child.is_complete()
        
    def set_left(self, node):
        """sets single child"""
        
        self.child = node
        node.parent = self

    def set_right(self, node):
        """sets single child"""
        
        self.child = node
        node.parent = self
        
    def get_right(self):
        """gets single child"""
        
        return self.child
    
    def get_evaluable(self):
        """returns Evaluable that computes a result from the child token"""
        
        return VariableFunction(self.operation_definition.token, (self.child.get_evaluable(), ))
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'NodeUnaryRight({self.operation_definition}, child={self.child})'


# ### NodeGroup

# In[16]:


class NodeGroup(NodeToken):
    """represents a grouping"""
    
    def __init__(self, group_definition, parent=None):
        self.parent = parent
        self.children = []
        
        self.group_definition = group_definition
        self.complete = False
        
        self.shape = {}
        self.sep_count = 0
    
    def is_complete(self, test_self=False):
        complete = test_self or self.complete
        complete &= all(c.is_complete() for c in self.children)
        return complete

    def close(self):
        self.sep_count = 0
        self.complete = True
        
        expected_size = 1
        for d,s in self.shape.items(): expected_size *= s
        
        if not self.group_definition.ignore_missing:
            assert len(self.children) == expected_size, f'Inconsistent dimensions shape={self.shape}, expected={expected_size}, actual={len(self.children)}'
    
    def set_right(self, node):
        self.children[-1] = node
        node.parent = self
        
    def get_right(self):
        return self.children[-1]

    def add(self, node):
        self.children.append(node)
        node.parent = self
        
        if len(self.shape) > 0 and self.sep_count >= len(self.shape):
            for i in range(len(self.shape), self.sep_count+1):
                self.shape[i-1] = self.shape.get(i-1, 1)
            self.shape[self.sep_count-1] += 1
            
        self.sep_count = 0
        
    def increase(self, depth=1):
        self.sep_count += depth
        
        if len(self.shape) == 0:
            self.shape[0] = 1
        
        # ensure minumum number of dimensions exists
        for i in range(len(self.shape), self.sep_count+1):
            self.shape[i-1] = self.shape.get(i-1, 1)
    
    def get_shape(self):
        shape = list(self.shape.items())
        shape.sort(key=lambda x:x[0], reverse=True)
        shape = tuple(s for d,s in shape)
        return shape
    
    def get_children(self):
        return self.children
    
    def get_evaluable(self):
        
        evaluables = [v.get_evaluable() for v in self.children]
        
        return VariableTensor(evaluables, self.get_shape(), self.group_definition.function)
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'NodeGroup({self.group_definition}, children={self.children})'


# ### NodeValue

# In[17]:


class NodeValue(NodeToken):
    """represents a value"""
    
    def __init__(self, value, value_type, parent=None):
        self.parent = parent
        self.value = value
        self.value_type = value_type
    
    def is_complete(self):
        return True
    
    def get_evaluable(self):
        """returns the approriate Evaluable for the tyoe of value this node holds"""

        value = None
        if self.value_type == TOKEN_TYPE_STRING:
            trimmed_string = self.value.strip(self.value[0])
            value = String(trimmed_string)
            value = VariableTensor([value], ())
            
        if self.value_type == TOKEN_TYPE_INTEGER:
            value = Integer(self.value)
            value = VariableTensor([value], ())
            
        if self.value_type == TOKEN_TYPE_NUMBER:
            value = Real(self.value)
            value = VariableTensor([value], ())
            
        if self.value_type == TOKEN_TYPE_LITERAL:
            value = Variable(self.value)
        
        return value
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'NodeValue({self.value}, {self.value_type})'


# ## Evaluable Tree Nodes

# ### Abstract Evaluable

# In[18]:


class Evaluable():
    """represents a node that can be evaluated"""
    
    def eval(self, environment, **kwargs):
        """performs the final evaluation returning an in environment value
        
        Arguments:
            Environment environment:  holds the current environment variables
                           **kwargs:  any arguments the Evaluable requires to evaluate
        """
        
        raise NotImplementedException('Evaluable.eval(environment)')


# ### VariableFunction

# In[19]:


class VariableFunction(Evaluable):
    
    def __init__(self, name, parameters):
        
        self.dtype = Evaluable
        self.name = name
        self.parameters = parameters
        if isinstance(parameters, VariableTensor):
            self.parameters = parameters.data
    
    def eval(self, environment, evaluable=False, **kwargs):
        
        if evaluable:
            return self
        
        assert self.name in environment, f'Function {self.name} not found'
        assert type(environment[self.name]) == FunctionSet, f'{self.name} is not a function'
        
        return environment[self.name].eval(environment, self.parameters)
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'VariableFunction_{self.name}({self.parameters})'


# ### Variable

# In[20]:


class Variable(Evaluable):
    
    def __init__(self, name):
        
        self.dtype = Evaluable
        self.name = name
    
    def eval(self, environment, references=False, evaluable=False, **kwargs):
        
        if references:
            return Tensor(Reference(self.name), ())
        
        if evaluable:
            return self
        
        if self.name not in environment:
            raise VariableNotDefined(self.name)
        
        value = environment[self.name]
        
        if type(value) == Evaluable:
            value = value.eval(environment)
        
        return value
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f"Variable({self.name})"


# ### VariableTensor

# In[21]:


class VariableTensor(Evaluable):
    
    def __init__(self, data, shape, function=None):
        
        self.dtype = Evaluable
        self.data = data
        self.shape = shape
        self.function = function
    
    def eval(self, environment, evaluable=False, **kwargs):
        
        if evaluable:
            return self
        
        values = [v.eval(environment, **kwargs) for v in self.data]
        
        if self.function == None and self.shape == ():
            return Tensor(values[:1], self.shape)
        else:
            return self.function(environment, values, self.shape, **kwargs)
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'VariableTensor({self.data}, {self.shape})'


# ## Data Structures

# ### Tensor

# In[22]:


def nd_index_from_shape(int_index, shape):
    devisor = 1
    devisors = [] if len(shape) == 0 else [devisor]
    for s in reversed(shape[1:]):
        devisor *= s
        devisors.append(devisor)
    index = []
    for devisor in reversed(devisors):
        i = int_index // devisor
        index.append(i)
        int_index -= i * devisor
    return index


# In[23]:


def count_end_zeros(data, sub=None):
    if sub:
        data = [d-s+1 for [d,s] in zip(data, sub)]
    c = 0
    for i in reversed(data):
        if i == 0:
            c += 1
        else:
            break
    return c


# In[24]:


class Tensor(Evaluable):
    """
    represents a value/tensor of any type, shape and rank
    """
    def __init__(self, data, shape=()):
        
        data = np.array(data, object)
        data = data.reshape((data.size,))
        
        assert data.size > 0, 'Tensor cannot be empty'
        
        if all(type(t) == Tensor for t in data):
            inner_shape = data[0].shape
            assert all(t.shape == inner_shape for t in data), 'Cannot combine tensors of different shapes'
            
            data = np.concatenate([t.data for t in data])
            shape = shape + inner_shape
        
        self._data = np.array(data, object).reshape(shape)
        self.data = self._data.reshape((self._data.size))
        
        self.first = self.data[0]
        self.shape = self._data.shape
        self.size = self._data.size
        self.rank = self._data.ndim
        self.dtype = type(self.data[0])
        
        assert all([type(i) == self.dtype for i in self.data]), 'All items in a Tensor must be of the same type'
        
    def __getitem__(self, index):
        
        data = self.data[index] if type(index) == int else self._data[index]
        shape = data.shape if type(data) == np.ndarray else ()
            
        return Tensor(data, shape)
        
    def __setitem__(self, index, value):
        
        if type(value) == Tensor:
            value = value._data
        
        if type(index) == int:
            self.data[index] = value
        else:
            self._data[index] = value
    
    def eval(self, environment, **kwargs):
        return self
    
    def __repr__(self):
        if self.rank == 0:
            return f'Tensor({self.data[()]})'
        else:
            return f'Tensor({self.data}, {self.shape})'
    
    def __str__(self):
        if self.rank == 0:
            return str(self.first)
        else:
            shape = list(self.shape)
            inner_size = shape.pop()
            strings = [str(i) for i in self.data]
            inner_lists = list(zip(*[iter(strings)]*inner_size))
            strings = ['['+', '.join(l)+']' for l in inner_lists]
            
            indexes = [nd_index_from_shape(i, shape) for i in range(len(strings))]
            
            left = [count_end_zeros(d) for d in indexes]
            left = [(len(shape) - i) * ' ' + i * '[' for i in left]

            right = [count_end_zeros(d, shape) for d in indexes]
            right = [i * ']' + ',' + i * '\n' for i in right]

            strings = [l+s+r for (l,s,r) in zip(left, strings, right)]
            strings[-1] = strings[-1].strip('\n,')

            string = '\n'.join(strings)
        
            return string


# ### Array

# In[25]:


class Array(Evaluable):
    
    def __init__(self, data):
        self.data = np.array(data, object)
        self.data = self.data.reshape((self.data.size,))
        self.size = self.data.size
        self.dtype = Array
            
    def __getitem__(self, index):
        if type(index) == int:
            return self.data[index]
        elif type(index) in [tuple, list]:
            if len(index) == 0:
                raise Exception('No index given in array item lookup')
            elif len(index) == 1:
                return self.data[index[0]]
            else:
                raise Exception('Too many indices given in array item lookup')
        else:
            return Array(self.data[index])
        
    def __setitem__(self, index, value):
        self.data[index] = value
    
    def eval(self, environment, **kwargs):
        return self
    
    def __repr__(self):
        return f'Array({self.data[()]})'
    
    def __str__(self):
        items = [str(i) for i in self.data]
        items = ', '.join(items)
        return f'({items})'


# ### FunctionSet

# In[26]:


class FunctionSet(Evaluable):
    
    def __init__(self, name, evaluation_paremeters=None):
        self.name = name
        self.signatures = {}
        self.evaluation_paremeters = evaluation_paremeters or {}
        
        self.dtype = FunctionSet
        
    def __contains__(self, partial_signature):
        l = len(partial_signature)
        for signature in self.signatures:
            if signature[:l] == partial_signature:
                return True
            
        return False
    
    def __getitem__(self, signature):
        return self.signatures[signature]
    
    def __setitem__(self, signature, value):
        par_names, function = value
        self.signatures[signature] = (par_names, function)
        
    def add(self, function_signature):
        self.signatures[function_signature.parameter_types] = function_signature
        
    def eval(self, environment, parameters, **kwargs):
        
        parameters = list(parameters)
        signature = [type(p) for p in parameters]
        
        for i, parameter in enumerate(parameters):
            eval_params = self.evaluation_paremeters.get(i, {})
            parameters[i] = parameter.eval(environment, **eval_params)
            signature[i] = parameters[i].dtype
        
        signature = tuple(signature)
        function_signature = None
        
        for signature_candidate in self.signatures:
            if len(signature) == len(signature_candidate) and all([a==b or a==None for a,b in zip(signature_candidate, signature)]):
                function_signature = self.signatures[signature_candidate]
        
#         assert signature in self.signatures, f'Signature {self.name}{tuple(p.__name__ for p in signature)} has no matching overload'
        assert function_signature != None, f'Signature {self.name}{tuple(p.__name__ for p in signature)} has no matching overload'
            
#         function_signature = self.signatures[signature]
        
        function = function_signature.function
        parameter_names = function_signature.parameter_names
        
        actual_shapes = [p.shape if type(p) == Tensor else () for p in parameters]
        actual_ranks = [len(s) for s in actual_shapes]
        
        ranks = [r if r!=None else a for r,a in zip(function_signature.parameter_ranks, actual_ranks)]
        extended_shapes = [s if r==0 else s[:-r] for s,r in zip(actual_shapes, ranks)]
        
        if len(ranks) == len(extended_shapes) == 0:
            extended_shape = []
        else:
            extended_shape = reduce(lambda x,y: x if len(x) > len(y) else y, extended_shapes)
        extended_ranks = [len(s) for s in extended_shapes]
        
        assert all([s in [extended_shape, ()] for s in extended_shapes]), f'Ranks, shape or extended shapes do not match'
        
        if extended_shape == ():
            return self.runFunction(function, environment, parameter_names, parameters)
        
        else:
            data = np.empty(extended_shape, dtype=object)
            
            for i in product(*[range(d) for d in extended_shape]):
                extracted_parameters = [p if r == 0 else p[i] for p, r in zip(parameters, extended_ranks)]
                
                data[i] = self.runFunction(function, environment, parameter_names, extracted_parameters)._data.tolist()
                    
            data = np.array(data.tolist())
            
            return Tensor(data, data.shape)
        
    def runFunction(self, function, environment, parameter_names, parameters):
        
        if parameter_names == False or parameter_names == None:
            return function(*parameters)
        
        elif parameter_names == True:
            return function(environment, *parameters)

        else:
            new_scoped_environment = environment.enterScope({k:v for k,v in zip(parameter_names, parameters)})
            return function(new_scoped_environment)
        
    def __repr__(self):
        return f'FunctionSet({self.name}, {self.signatures})'
    
    def __str__(self):
        if len(self.signatures) == 0:
            parameter_types = ''
        if len(self.signatures) == 1:
            parameter_types = next(iter(self.signatures))
            parameter_types = ['Any' if t == None else t.__name__ for t in parameter_types]
            parameter_types = ', '.join(parameter_types)
        else:
            parameter_types = '...'
            
        name = '<AnonymousFunction>' if self.name == '' else self.name
            
        return f'{name}({parameter_types})'


# ### ConversionFunctionSet

# In[27]:


class ConversionFunctionSet(Evaluable):
    
    def __init__(self, name, forwards, backwards):
        self.name = name
        self.forwards = forwards
        self.backwards = backwards
        self.dtype = ConversionFunctionSet
    
    def eval(self, environment, tensor, forwards=True, **kwargs):
        shape = tensor.shape
        data = tensor.data
        
        if forwards:
            converted_data = [self.forwards(d) for d in data]
        else:
            converted_data = [self.backwards(d) for d in data]
            
        return Tensor(converted_data, shape)
    
    def __repr__(self):
        return f'ConversionFunctionSet({self.name})'
    
    def __str__(self):
        return f'<{self.name}>'


# ## Data Types

# ### Abstract Data

# In[28]:


class Data(Evaluable):
    pass


# ### String

# In[29]:


class String(Data):
    
    def __init__(self, value):
        self.value = value
    
    def eval(self, environment, **kwargs):
        return self
    
    def __repr__(self):
        return f'String("{self.value}")'
    
    def __str__(self):
        return f'"{self.value}"'


# ### Integer

# In[30]:


class Integer(Data):
    
    def __init__(self, value):
        self.value = value
    
    def eval(self, environment, **kwargs):
        return self


# ### Real

# In[31]:


class Real(Data):
    
    def __init__(self, value):
        self.value = Decimal(value)
    
    def eval(self, environment, **kwargs):
        return self
    
    def __repr__(self):
        return f'Real({str(self.value)})'
    
    def __str__(self):
        return str(self.value)


# ### Complex

# In[ ]:





# ### Boolean

# In[32]:


class Boolean(Data):
    
    def __init__(self, value):
        self.value = value
    
    def eval(self, environment, **kwargs):
        return self


# ### FunctionSignature

# In[33]:


class FunctionSignature():
    
    def __init__(self, name, function, parameter_names, parameter_types, parameter_ranks=None, parameter_shapes=None):
        
        self.name = name
        self.function = function
        self.parameter_count = len(parameter_types)
        self.parameter_names = parameter_names
        self.parameter_types = parameter_types
        self.parameter_ranks = parameter_ranks or self.parameter_count*(None,)
        self.parameter_shapes = parameter_shapes or self.parameter_count*(None,)
        
    def __repr__(self):
        return f'FunctionSignature{(self.name, self.function, self.parameter_names, self.parameter_types, self.parameter_ranks, self.parameter_shapes)}'
    
    def __str__(self):
        parameter_types = [str(t) for t in self.parameter_types]
        parameter_types = ', '.join(parameter_types)
        return f'{self.name}({parameter_types})'


# ### Reference

# In[34]:


class Reference(Data):
    
    def __init__(self, value):
        self.value = value
    
    def eval(self, environment, **kwargs):
        return self


# ## BuiltIns

# In[35]:


class BuiltIns():
    
    def __init__(self):
        self.functions = []
        self.function_parameter_evaluation_parameters = {}
        self.vars = []
        self.binary_operators = []
        self.binary_operators_continuing = []
        self.left_unary_operators = []
        self.right_unary_operators = []
        self.groups = []
        self.new_items = []
        self.conversion_function_sets = []
        
    def register_function(self, name, function, parameter_names, parameter_types, parameter_ranks=None, parameter_shapes=None):
        self.functions.append((name, function, parameter_names, parameter_types, parameter_ranks, parameter_shapes))
        
    def set_evaluation_parameter(self, function_name, parameter_index, key, value):
        parameter_list = self.function_parameter_evaluation_parameters.get(function_name, {})
        parameters = parameter_list.get(parameter_index, {})
        parameters[key] = value
        parameter_list[parameter_index] = parameters
        self.function_parameter_evaluation_parameters[function_name] = parameter_list
        
    def register_binary_operator(self, name, precedence, continuing=False):
        if continuing:
            self.binary_operators_continuing.append(TokenOperandDefinition(name, precedence))
        
        self.binary_operators.append(TokenOperandDefinition(name, precedence))
        
    def register_left_unary_operator(self, name, precedence):
        self.left_unary_operators.append(TokenOperandDefinition(name, precedence))
        
    def register_right_unary_operator(self, name, precedence):
        self.right_unary_operators.append(TokenOperandDefinition(name, precedence))
        
    def register_var(self, name, value):
        self.vars.append((name, value))
        
    def register_grouping(self, open_token, close_token, seperators, ignore_missing, function):
        self.groups.append(TokenGroupDefinition(open_token, close_token, seperators, ignore_missing, function))
        
    def register_new_item_seperator(self, token):
        self.new_items.append(TokenNewItemDefinition(token))
        
    def register_conversion_function_set(self, name, forwards, backwards):
        self.conversion_function_sets.append((name, forwards, backwards))
        
        
built_ins = BuiltIns()


# # Built In Functions, Operators and Variables

# ### Groups

# #### Group ( )

# In[36]:


def group_round(environment, items, shape, force_array=False, **kwargs):
    
    if shape == () and len(items) > 0 and force_array == False:
        return items[0]
    else:
        return Array(items)

built_ins.register_grouping('(', ')', {',': 1, '\n': 1}, True, group_round)


# #### Group [ ]

# In[37]:


def group_squre(environment, items, shape, **kwargs):
    
    assert len(items) > 0, 'Tensors can not be empty'
    
    base_shape = items[0].shape
    assert all([i.shape == base_shape for i in items]), 'Tensor elements have inconsistent shapes'
    
    extended_shape = shape + base_shape
    data = np.array([i.data for i in items]).reshape(extended_shape)
    
    return Tensor(data, extended_shape)

built_ins.register_grouping('[', ']', {',': 1, ';': 2, '\n': 0}, False, group_squre)


# #### Group { }

# In[38]:


def group_curly(environment, items, shape, **kwargs):
    return items[-1]

built_ins.register_grouping('{', '}', {';': 1, '\n': 1}, True, group_curly)


# #### Group | |

# In[39]:


def group_straight(environment, items, shape, **kwargs):
    
    assert shape == (), 'Cannot take absolute value of an array'
    assert items[0].dtype == Real, 'Cannot take absolute value of non Real value'
    
#     return Tensor(Real(abs(items[0].first.value)))

    return VariableFunction('abs', items).eval(environment)

built_ins.register_grouping('|', '|', {}, True, group_straight)
built_ins.register_grouping('||', '||', {}, True, group_straight)


# ### New Item Seperators

# In[40]:


built_ins.register_new_item_seperator(',')
built_ins.register_new_item_seperator(';')
built_ins.register_new_item_seperator('\n')


# ### Variabels

# In[41]:


built_ins.register_var('PI', Tensor([Real('3.141592653589793238462643383279502884197')]))
built_ins.register_var('e', Tensor([Real('2.718281828459045235360287471352662497757')]))
built_ins.register_var('phi', Tensor([Real('1.61803398874989484820458683436563811772')]))


# ### Declare Operations

# In[42]:


# Unary Operations: -, +
built_ins.register_left_unary_operator('+', 7)
built_ins.register_left_unary_operator('-', 7)
built_ins.register_left_unary_operator('=', 0)

# Binary Operations:

# arithmetic
built_ins.register_binary_operator('+',   3, True)
built_ins.register_binary_operator('-',   3, True)
built_ins.register_binary_operator('*',   4, True)
built_ins.register_binary_operator('4',   4)
built_ins.register_binary_operator('/',   4, True)
built_ins.register_binary_operator('//',  4, True)
# built_ins.register_binary_operator('%',   4, True)
built_ins.register_binary_operator('mod', 4, True)
built_ins.register_binary_operator('^',   5, True)

# matrix
built_ins.register_binary_operator('#',   4, True)
built_ins.register_binary_operator('matmul', 4, True)

# vector
built_ins.register_binary_operator('.*' , 4, True)
built_ins.register_binary_operator('dot', 4, True)

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
built_ins.register_binary_operator('@', -1, True)


# ### Register Functions

# #### Assignment: =

# In[43]:


def assignment(environment, key, value):
    
    if type(key) == Array:
        for k, v in zip(key, value):
            assignment(environment, k, v)
    else:
        environment[key.first.value] = value
        
    return value

def post_assignment(environment, key):
    value = environment['']
    return assignment(environment, key, value)

built_ins.register_function('=', assignment, True, (Array, None))
built_ins.register_function('=', assignment, True, (Reference, None))
built_ins.register_function('=', post_assignment, True, (Reference,))


# #### Function Definition: =>

# In[44]:


def define_function(environment, parameters, evaluable):
    
    if type(parameters) == Tensor and parameters.dtype == Reference:
        parameter_names = [parameters.first.value]
    elif type(parameters) == Array:
        parameter_names = [p.first.value for p in parameters.data]
    elif type(parameters) == tuple:
        parameter_names = list(parameters)
    
    parameter_types = tuple([None] * len(parameter_names))
    
    def function(environment):
        return evaluable.eval(environment)
    
    function_signature = FunctionSignature('', function, parameter_names, parameter_types, parameter_ranks=None, parameter_shapes=None)

    function_set = FunctionSet('')
    function_set.add(function_signature)
    
    return function_set

built_ins.register_function('=>', define_function, True, (Reference, None))
built_ins.register_function('=>', define_function, True, (Array, None))


# #### Unary Operations: -, +

# In[45]:


built_ins.register_function('+', lambda t:Tensor(Real(+t.first.value)), None, (Real,), (0,))
built_ins.register_function('-', lambda t:Tensor(Real(-t.first.value)), None, (Real,), (0,))


# #### Binary Operantors: +, -, *, /, //, %, ^

# In[46]:


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


# #### Matrix Multiplication: # #

# In[47]:


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


# #### Vector Dot Product: .*

# In[48]:


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


# #### Absolute value abs

# In[49]:


def absolute(A):
    return Tensor(Real(abs(A.first.value)))

built_ins.register_function('abs', absolute, None, (Real,), (0,))


# #### Root and Square root $

# In[50]:


def root(A, B):
    return Tensor(Real(B.first.value ** (Decimal(1) / A.first.value)))

def sqrt(A):
    return Tensor(Real(A.first.value ** Decimal(0.5)))

built_ins.register_function('$', sqrt, None, (Real,), (0,))
built_ins.register_function('$', root, None, (Real, Real), (0, 0))


# #### Function Call

# In[51]:


def function_call(environment, function_set, parameters):
    return function_set.eval(environment, parameters)

built_ins.register_function('9', function_call, True, (FunctionSet, Array))


def foo(A):
    return Tensor(Real(A.first.value * A.first.value))
def bar(A, B):
    return Tensor(Real(A.first.value * B.first.value))
    
built_ins.register_function('fun', foo, False, (Real,), (0,))
built_ins.register_function('fun', bar, False, (Real, Real), (0, 0))


# #### Tensor Lookup

# In[52]:


def tensor_lookup(environment, tensor, parameters):
    index = [int(p.first.value) for p in parameters]
    return tensor[tuple(index)]

built_ins.register_function('9', tensor_lookup, True, (Real, Array))


# #### Array Lookup

# In[53]:


def array_lookup(environment, array, parameters):
    index = [int(p.first.value) for p in parameters]
    return array[tuple(index)]

built_ins.register_function('9', array_lookup, True, (Array, Array))


# #### Conversion @, [implocit]

# In[54]:


def conversion_forwards_function_call(environment, tensor, conversion_function_set):
    return conversion_function_set.eval(environment, tensor, True)

def conversion_backwards_function_call(environment, tensor, conversion_function_set):
    return conversion_function_set.eval(environment, tensor, False)

built_ins.register_function('9', conversion_forwards_function_call, True, (None, ConversionFunctionSet))
built_ins.register_function('@', conversion_backwards_function_call, True, (None, ConversionFunctionSet))


# ### Conversion Specifiers

# #### Distance

# In[55]:


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


def in_forwards(_in):
    return Real(_in.value * Decimal('0.0254'))

def in_backwards(m):
    return Real(m.value / Decimal('0.0254'))

def ft_forwards(ft):
    return Real(ft.value * Decimal('0.3048'))

def ft_backwards(m):
    return Real(m.value / Decimal('0.3048'))

def yd_forwards(yd):
    return Real(yd.value * Decimal('0.9144'))

def yd_backwards(m):
    return Real(m.value / Decimal('0.9144'))

def mi_forwards(mi):
    return Real(mi.value * Decimal('1609.344'))

def mi_backwards(m):
    return Real(m.value / Decimal('1609.344'))

built_ins.register_conversion_function_set('km', km_forwards, km_backwards)
built_ins.register_conversion_function_set( 'm',  m_forwards,  m_backwards)
built_ins.register_conversion_function_set('cm', cm_forwards, cm_backwards)
built_ins.register_conversion_function_set('mm', mm_forwards, mm_backwards)
built_ins.register_conversion_function_set('um', um_forwards, um_backwards)
built_ins.register_conversion_function_set('nm', nm_forwards, nm_backwards)
built_ins.register_conversion_function_set('pm', pm_forwards, pm_backwards)

built_ins.register_conversion_function_set('in', in_forwards, in_backwards)
built_ins.register_conversion_function_set('ft', ft_forwards, ft_backwards)
built_ins.register_conversion_function_set('yd', yd_forwards, yd_backwards)
built_ins.register_conversion_function_set('mi', mi_forwards, mi_backwards)


# #### Area

# In[56]:


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


# #### Volume

# In[57]:


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


# #### Time

# In[58]:


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


# # Define Token

# ## Tokens Types

# In[59]:


TOKEN_TYPE_STRING     = 'string'
TOKEN_TYPE_INTEGER    = 'integer'
TOKEN_TYPE_NUMBER     = 'number'
TOKEN_TYPE_OPERATOR   = 'operand'
TOKEN_TYPE_OPEN_GROUP = 'group'
TOKEN_TYPE_LITERAL    = 'literal'

TOKEN_TYPE_OPEN_GROUP        = 'open group'
TOKEN_TYPE_CLOSE_GROUP       = 'close group'
TOKEN_TYPE_NEW_ITEM          = 'new item'
TOKEN_TYPE_BINARY            = 'binary operand'
TOKEN_TYPE_BINARY_CONTINUING = 'continuing binary operand'
TOKEN_TYPE_UNARY_LEFT        = 'left unary operand'
TOKEN_TYPE_UNARY_RIGHT       = 'right unary operand'

OPERAND_TYPES = [
    TOKEN_TYPE_OPEN_GROUP,
    TOKEN_TYPE_CLOSE_GROUP, 
    TOKEN_TYPE_NEW_ITEM, 
    TOKEN_TYPE_BINARY, 
    TOKEN_TYPE_BINARY_CONTINUING, 
    TOKEN_TYPE_UNARY_LEFT, 
    TOKEN_TYPE_UNARY_RIGHT, 
]

TOKEN_TYPE_VALUE = [
    TOKEN_TYPE_STRING,
    TOKEN_TYPE_INTEGER,
    TOKEN_TYPE_NUMBER,
    TOKEN_TYPE_LITERAL,
]


# ## Token Operations

# In[60]:


token_definitions = {
    TOKEN_TYPE_OPEN_GROUP:        built_ins.groups,
    TOKEN_TYPE_CLOSE_GROUP:       built_ins.groups, 
    TOKEN_TYPE_NEW_ITEM:          built_ins.new_items, 
    TOKEN_TYPE_BINARY:            built_ins.binary_operators, 
    TOKEN_TYPE_BINARY_CONTINUING: built_ins.binary_operators_continuing, 
    TOKEN_TYPE_UNARY_LEFT:        built_ins.left_unary_operators, 
    TOKEN_TYPE_UNARY_RIGHT:       built_ins.right_unary_operators, 
}


# ## Operation Indexing

# In[61]:


def find_token_definition(string, token_type, f = lambda x:x.token):
    for token_definition in token_definitions[token_type]:
        if string == f(token_definition):
#         if re.fullmatch(operator.re_match, string) != None:
            return token_definition
    return None


# ## Define Token Regular Expressions

# In[62]:


def re_join(l, f=lambda x:x):
    items = [f(i) for i in l]
    items.sort(key=lambda x:len(x), reverse=True)
    return '(' + ')|('.join([re.escape(i) for i in items]) + ')'

# regex
re_number =    r"""((([\.][0-9]+)|([0-9]+[\.]?[0-9]*))([eE][-+]?[0-9]+)?)"""
re_integer =   r"""((0b|0o|0d|0x|[0-9]+_)[0-9a-zA-Z,]+)"""
re_string =    r"""((\""".*?\""")|('''.*?''')|(".*?")|('.*?'))"""
re_literal =   r"""([A-Za-z_][A-Za-z0-9_]*)"""


re_open_group =                 re_join(built_ins.groups, lambda x:x.open_token)
re_close_group =                re_join(built_ins.groups, lambda x:x.close_token)
re_binary_operands =            re_join(built_ins.binary_operators, lambda x:x.token)
re_binary_continuing_operands = re_join(built_ins.binary_operators_continuing, lambda x:x.token)
re_left_unary_operands =        re_join(built_ins.left_unary_operators, lambda x:x.token)
re_right_unary_operands =       re_join(built_ins.right_unary_operators, lambda x:x.token)
re_new_item =                   re_join(built_ins.new_items, lambda x:x.token)


re_tokens = {
    TOKEN_TYPE_STRING:            re_string,
    TOKEN_TYPE_INTEGER:           re_integer,
    TOKEN_TYPE_NUMBER:            re_number,
    TOKEN_TYPE_LITERAL:           re_literal,
    TOKEN_TYPE_OPEN_GROUP:        re_open_group,
    TOKEN_TYPE_BINARY:            re_binary_operands,
    TOKEN_TYPE_BINARY_CONTINUING: re_binary_continuing_operands,
    TOKEN_TYPE_UNARY_LEFT:        re_left_unary_operands,
    TOKEN_TYPE_UNARY_RIGHT:       re_right_unary_operands,
    TOKEN_TYPE_NEW_ITEM:          re_new_item,
    TOKEN_TYPE_CLOSE_GROUP:       re_close_group,
}

re_tokens


# # Parse

# ## Lexing

# In[63]:


def re_match_length(string, re_pattern):
    match = re.match(re_pattern, string)
    return match.span()[1] if match != None else 0


# In[64]:


class Lexer:
    def __init__(self, ans_available=False):
        self.tokens = []
        self.ans_available = ans_available
        
        self.source_string = ''
        self.current_ln_offset = 0
        self.ln_count = 0
        self.source = Source()
        
    def process(self, string):
        # TOKEN_TYPE_STRING
        # TOKEN_TYPE_INTEGER
        # TOKEN_TYPE_NUMBER
        # TOKEN_TYPE_LITERAL

        # TOKEN_TYPE_OPEN_GROUP
        # TOKEN_TYPE_BINARY
        # TOKEN_TYPE_BINARY_CONTINUING
        # TOKEN_TYPE_UNARY_LEFT
        # TOKEN_TYPE_UNARY_RIGHT
        # TOKEN_TYPE_NEW_ITEM
        # TOKEN_TYPE_CLOSE_GROUP
        
        tokens = []
        
        i = len(self.source_string)
        string = self.source_string = self.source_string + string
        self.source.set(string)
        
        while i < len(string):

            if string[i] in ' ':
                i += 1
                continue
                
            offset = i - self.current_ln_offset
            ln = self.ln_count
            
            if string[i] == '\n':
                self.current_ln_offset = i+1
                self.ln_count += 1

            if len(tokens) > 0:
                last_token_type =  tokens[-1].token_type
            elif len(self.tokens) > 0:
                last_token_type = self.tokens[-1].token_type
            else:
                last_token_type = None
                
            allowed_token_types = []
            allowed_token_types_with_implicit_op = {}
            allowed_token_types_with_ans = {}

            # begin with
            if last_token_type in [
                None,
            ]:

                allowed_token_types = [
                    TOKEN_TYPE_UNARY_LEFT,
                    TOKEN_TYPE_OPEN_GROUP,
                    TOKEN_TYPE_NEW_ITEM,
                    TOKEN_TYPE_CLOSE_GROUP,
                    *TOKEN_TYPE_VALUE,
                ]
                if self.ans_available:
                    allowed_token_types_with_ans = {
                        TOKEN_TYPE_UNARY_RIGHT: '',
                        TOKEN_TYPE_BINARY_CONTINUING: '',
                    }

            if last_token_type in [                TOKEN_TYPE_OPEN_GROUP,
                TOKEN_TYPE_NEW_ITEM,
            ]:
                allowed_token_types = [
                    TOKEN_TYPE_UNARY_LEFT,
                    TOKEN_TYPE_OPEN_GROUP,
                    TOKEN_TYPE_NEW_ITEM,
                    TOKEN_TYPE_CLOSE_GROUP,
                    *TOKEN_TYPE_VALUE,
                ]

            # after value excluding literal
            if last_token_type in [
                TOKEN_TYPE_CLOSE_GROUP,
                TOKEN_TYPE_UNARY_RIGHT,
                TOKEN_TYPE_STRING,
                TOKEN_TYPE_INTEGER,
                TOKEN_TYPE_NUMBER,
            ]:
                allowed_token_types = [
                    TOKEN_TYPE_UNARY_RIGHT,
                    TOKEN_TYPE_BINARY,
                    TOKEN_TYPE_NEW_ITEM,
                    TOKEN_TYPE_CLOSE_GROUP,
                ]
                allowed_token_types_with_implicit_op = {
                    TOKEN_TYPE_OPEN_GROUP: '9',
                    TOKEN_TYPE_LITERAL: '9',
                }

            # after literal value
            if last_token_type in [
                TOKEN_TYPE_LITERAL,
            ]:
                allowed_token_types = [
                    TOKEN_TYPE_UNARY_RIGHT,
                    TOKEN_TYPE_BINARY,
                    TOKEN_TYPE_NEW_ITEM,
                    TOKEN_TYPE_CLOSE_GROUP,
                ]
                allowed_token_types_with_implicit_op = {
                    TOKEN_TYPE_OPEN_GROUP: '9',
                    TOKEN_TYPE_LITERAL: '9',
                }

            # after operator
            if last_token_type in [
                TOKEN_TYPE_BINARY,
                TOKEN_TYPE_BINARY_CONTINUING,
                TOKEN_TYPE_UNARY_LEFT,

            ]:
                allowed_token_types = [
                    TOKEN_TYPE_OPEN_GROUP,
                    TOKEN_TYPE_UNARY_LEFT,
                    *TOKEN_TYPE_VALUE,
                ]


            # find matching token type
            token_type, token_str = None, None

            all_allowed_token_types = [
                list(allowed_token_types_with_ans.items()),
                [(t, None) for t in allowed_token_types],
                list(allowed_token_types_with_implicit_op.items()),
            ]
            all_allowed_token_types = sum(all_allowed_token_types, [])

            for possible_token_type, implicit_op in all_allowed_token_types:
                re_pattern = re_tokens[possible_token_type]

                l = re_match_length(string[i:], re_pattern)
                if l > 0:

                    if implicit_op == '':
                        tokens.append(Token(TOKEN_TYPE_LITERAL, implicit_op, ln, offset, self.source))
                    elif implicit_op != None:
                        tokens.append(Token(TOKEN_TYPE_BINARY, implicit_op, ln, offset, self.source))

                    token_type = possible_token_type
                    token_str = string[i:i+l]
                    break



            # invalid token
            if token_type == None:
                raise TokenNotAllowedException(self.source, ln, offset)
                i += 1
            else:
                tokens.append(Token(token_type, token_str, ln, offset, self.source))
                i += len(token_str)

        self.tokens += tokens
        return tokens  


# ## Treeify

# In[65]:


def bubble_up(focus, new):
    """
    Finds ancestor/parent in tree upwards from `token` thats the first group token or the first
    """
    
    while True:
        if type(focus) == NodeGroup or focus.precedence < new.precedence:
            return focus
        else:
            focus = focus.parent


# In[66]:


def bubble_up_to_group(focus):
    while True:
        if type(focus) == NodeGroup:
            return focus
        else:
            focus = focus.parent


# In[67]:


class TokenTreeBuilder:
    
    def __init__(self):
        self.root = NodeGroup(find_token_definition('{', TOKEN_TYPE_OPEN_GROUP, lambda x:x.open_token), None)
        self.focus = self.root

    def build(self, tokens):
    
        # TOKEN_TYPE_STRING
        # TOKEN_TYPE_INTEGER
        # TOKEN_TYPE_NUMBER
        # TOKEN_TYPE_LITERAL

        # TOKEN_TYPE_OPEN_GROUP
        # TOKEN_TYPE_BINARY
        # TOKEN_TYPE_UNARY_LEFT
        # TOKEN_TYPE_UNARY_RIGHT

        # TOKEN_TYPE_NEW_ITEM
        # TOKEN_TYPE_CLOSE_GROUP

        for token in tokens:


            # focus is
            # Binary Operator
            # Left Unary Operator
            if type(self.focus) in [
                NodeBinary,
                NodeUnaryLeft,
            ]:

                # next is 
                # Unary left
                if token.token_type == TOKEN_TYPE_UNARY_LEFT:

                    operand = find_token_definition(token.string, TOKEN_TYPE_UNARY_LEFT)
                    next_node = NodeUnaryLeft(operand)

                    self.focus.set_right(next_node)
                    self.focus = next_node

                # next is
                # Group
                elif token.token_type == TOKEN_TYPE_OPEN_GROUP:

                    group = find_token_definition(token.string, TOKEN_TYPE_OPEN_GROUP, lambda x:x.open_token)
                    next_node = NodeGroup(group)
                    self.focus.set_right(next_node)
                    self.focus = next_node

                # next is
                # TOKEN_TYPE_STRING
                # TOKEN_TYPE_INTEGER
                # TOKEN_TYPE_NUMBER
                # TOKEN_TYPE_LITERAL
                elif token.token_type in TOKEN_TYPE_VALUE:

                    next_node = NodeValue(token.string, token.token_type)
                    self.focus.set_right(next_node)
                    self.focus = next_node

                else:
                    raise TokenNotAllowedException(token)


            # focus is
            # Value
            # Closed Group
            elif type(self.focus) == NodeValue or (type(self.focus) == NodeGroup and self.focus.is_complete()):

                # next is
                # Binary
                if token.token_type in [TOKEN_TYPE_BINARY, TOKEN_TYPE_BINARY_CONTINUING]:

                    operand = find_token_definition(token.string, TOKEN_TYPE_BINARY)
                    next_node = NodeBinary(operand)

                    parent_node = bubble_up(self.focus.parent, next_node)
                    child_node = parent_node.get_right()
                    parent_node.set_right(next_node)
                    next_node.set_left(child_node)
                    self.focus = next_node


                # next is
                # Unary right
                elif token.token_type == TOKEN_TYPE_UNARY_RIGHT:

                    operand = find_token_definition(token.string, TOKEN_TYPE_UNARY_RIGHT)
                    next_node = NodeUnaryRight(operand)

                    parent_node = self.focus.parent # bubble_up(self.focus.parent, next_node)
                    child_node = parent_node.get_right()
                    parent_node.set_right(next_node)
                    next_node.set_left(child_node)
                    # self.focus = next_node

                # next is
                # New item
                elif token.token_type == TOKEN_TYPE_NEW_ITEM:

                    token_definition = find_token_definition(token.string, TOKEN_TYPE_NEW_ITEM)

                    parent_node = bubble_up_to_group(self.focus.parent)

                    if token_definition.token in parent_node.group_definition.seperators:

                        depth = parent_node.group_definition.seperators[token_definition.token]
                        if depth > 0:
                            parent_node.increase(depth)
                            self.focus = parent_node
                    else:
                        raise TokenNotAllowedException(token)


                # next is
                # Close group
                elif token.token_type == TOKEN_TYPE_CLOSE_GROUP:

                    parent_node = bubble_up_to_group(self.focus.parent)
                    parent_node.close()
                    self.focus = parent_node

                # next is
                else:
                    raise TokenNotAllowedException(token)


            # focus is
            # Open Group
            elif type(self.focus) == NodeGroup and not self.focus.is_complete(): 

                # next is
                # Binary - use ans on left
                if token.token_type == TOKEN_TYPE_BINARY:

                    left = NodeValue('ans', TOKEN_TYPE_LITERAL)

                    operand = find_token_definition(token.string, TOKEN_TYPE_BINARY)
                    next_node = NodeBinary(operand)
                    next_node.set_left(left)

                    self.focus.add(next_node)
                    self.focus = next_node

                # next is
                # Unary left
                elif token.token_type == TOKEN_TYPE_UNARY_LEFT:

                    operand = find_token_definition(token.string, TOKEN_TYPE_UNARY_LEFT)
                    next_node = NodeUnaryLeft(operand)

                    self.focus.add(next_node)
                    self.focus = next_node

                # next is
                # Group
                elif token.token_type == TOKEN_TYPE_OPEN_GROUP:

                    group = find_token_definition(token.string, TOKEN_TYPE_OPEN_GROUP, lambda x:x.open_token)
                    next_node = NodeGroup(group)
                    self.focus.add(next_node)
                    self.focus = next_node

                # next is
                # Close Group
                elif token.token_type == TOKEN_TYPE_CLOSE_GROUP:

                    self.focus.close()

                # next is
                # TOKEN_TYPE_STRING
                # TOKEN_TYPE_INTEGER
                # TOKEN_TYPE_NUMBER
                # TOKEN_TYPE_LITERAL
                elif token.token_type in TOKEN_TYPE_VALUE:

                    next_node = NodeValue(token.string, token.token_type)
                    self.focus.add(next_node)
                    self.focus = next_node

                # next is 
                # TOKEN_TYPE_NEW_ITEM
                elif token.token_type == TOKEN_TYPE_NEW_ITEM:

                    token_definition = find_token_definition(token.string, TOKEN_TYPE_NEW_ITEM)

                    if token_definition.token in self.focus.group_definition.seperators:

                        depth = self.focus.group_definition.seperators[token_definition.token]
                        if depth > 0:
                            self.focus.increase(depth)
                    else:
                        raise TokenNotAllowedException(token)

                # next is
                else:
                    raise TokenNotAllowedException(token)



        return self.root


# ## Computation Graph

# In[68]:


def build_computation_graph(token_tree):
    return token_tree.get_evaluable()


# # Excecute

# ## Environment

# In[69]:


class Environment():
       
    def __init__(self, parent=None, dictionary=None):
        self.parent = parent
        self.dictionary = dictionary or {}
        self.ln_count = 1
        self.ans_available = False
        
    def __getitem__(self, key):
        
        if key in self.dictionary:
            return self.dictionary[key]
        elif self.parent != None:
            return self.parent[key]
        else:
            assert False, f'key {key} is not defined in this scope'
        
    def __setitem__(self, key, value):
        
        if type(key) in [list, tuple] and type(value) in [list, tuple]:
            for k,v in zip(key, value):
                self[key] = value
        
        else:
            if key in self.dictionary:
                self.dictionary[key] = value
            elif self.parent != None:
                self.parent[key] = value
            else:
                self.dictionary[key] = value
    
    def __contains__(self, key):
        
        if key in self.dictionary:
            return True
        elif self.parent != None:
            return key in self.parent
        else:
            return False
        
    def getLnCount(self):
        return str(self.ln_count)
        
    def addLn(self, value, code, environment):
        in_name = f'in{self.ln_count}'
        out_name = f'out{self.ln_count}'
        self[in_name] = define_function(environment, (), code)
        self[out_name] = value
        self[''] = value
        
        self.ln_count += 1
        self.ans_available = True
        
        return out_name
    
    def enterScope(self, dictionary=None):
        return Environment(self, dictionary)
        
    def exitScope(self):
        return self if self.parent == None else self.parent
        
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'Environment({self.dictionary, self.parent})'


# In[70]:


def create_base_environment():
    built_in_variables = {k:v for k,v in built_ins.vars}
    built_in_functions = {}
    built_in_conversion_function_sets = {}
    
    for name, function, parameter_names, parameter_types, parameter_ranks, parameter_shapes in built_ins.functions:
        
        parameter_evaluation_parameters = built_ins.function_parameter_evaluation_parameters.get(name, {})
        
        built_in_functions[name] = built_in_functions.get(name, FunctionSet(name, parameter_evaluation_parameters))
        built_in_functions[name].add(FunctionSignature(
            name, 
            function, 
            parameter_names, 
            parameter_types, 
            parameter_ranks, 
            parameter_shapes
        ))
        
    for name, forward, reverse in built_ins.conversion_function_sets:
        built_in_conversion_function_sets[name] = ConversionFunctionSet(name, forward, reverse)
    
    environment = Environment(None, {**built_in_variables, **built_in_functions, **built_in_conversion_function_sets})
    
    return environment


# ## Evaluate

# In[71]:


def evaluate(computation_graph, environment):
    return computation_graph.eval(environment)


# In[72]:


def read(string, environment, lexer=None, token_tree_builder=None, **kwargs):
    
    lexer = lexer or Lexer(environment.ans_available)
    tokens = lexer.process(string)
    
    token_tree_builder = token_tree_builder or TokenTreeBuilder()
    token_tree = token_tree_builder.build(tokens)
    is_complete = token_tree.is_complete(True)
    
    return {
        'environment': environment,
        'lexer':       lexer,
        'token_tree_builder': token_tree_builder,
        'is_complete': is_complete,
    }


# In[73]:


def execute(token_tree_builder, environment, **kwargs):
    computation_graph = build_computation_graph(token_tree_builder.root)
    result = evaluate(computation_graph, environment)
    ln_name = environment.addLn(result, computation_graph, environment)
    print_result(result, ln_name)

    return result


# In[74]:


def print_result(result, ln_name):
    ln_name = ln_name + ': '
    space = ' ' * len(ln_name)
    lines = str(result).split('\n')
    pre = [ln_name] + (len(lines)-1) * [space]
    
    lines = [p+l for p,l in zip(pre, lines)]
    
    print(*lines, sep='\n')


# ## Run

# In[75]:


def calc(query, environment, debug=False):

    context = read(query, environment)
    result = execute(**context)
    return result



os.system('title Calculator')

environment = create_base_environment()
while True:
    try:
        in_name = environment.getLnCount()
        command = input(f' in{in_name}> ')
        if command.strip() == '':
            continue
        if command.strip() == 'exit':
            break

        context = read(command, environment)

        while not context['is_complete']:
            command = '\n' + input(' ' * len(in_name) + '   > ')
            context = read(command, **context)

        execute(**context)
        print('')

    except KeyboardInterrupt:
        # print('\nexiting...')
        # break

        if '' in environment:
            pyperclip.copy(str(environment[''].first.value))
            print('\ncopied to clipboard')
        else:
            print('\nnothing to copy')
        continue
    except Exception as exception:
        print(exception)