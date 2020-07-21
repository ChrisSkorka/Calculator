from decimal import Decimal
from Classes.evaluable_tree_nodes import Evaluable



class Data(Evaluable):
    pass



class String(Data):
    
    def __init__(self, value):
        self.value = value
    
    def eval(self, environment, **kwargs):
        return self
    
    def __repr__(self):
        return f'String("{self.value}")'
    
    def __str__(self):
        return f'"{self.value}"'



class Integer(Data):
    
    def __init__(self, value):
        self.value = value
    
    def eval(self, environment, **kwargs):
        return self



class Complex(Data):
    pass



class Real(Data):
    
    def __init__(self, value):
        self.value = Decimal(value)
    
    def eval(self, environment, **kwargs):
        return self
    
    def __repr__(self):
        return f'Real({str(self.value)})'
    
    def __str__(self):
        return str(self.value)



class Boolean(Data):
    
    def __init__(self, value):
        self.value = value
    
    def eval(self, environment, **kwargs):
        return self



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



class Reference(Data):
    
    def __init__(self, value):
        self.value = value
    
    def eval(self, environment, **kwargs):
        return self