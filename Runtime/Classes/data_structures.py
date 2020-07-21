import numpy as np
from Classes.evaluable_tree_nodes import Evaluable



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