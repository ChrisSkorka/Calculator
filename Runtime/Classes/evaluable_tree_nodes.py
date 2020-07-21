from Classes.data_structures import *



class Evaluable():
    """represents a node that can be evaluated"""
    
    def eval(self, environment, **kwargs):
        """performs the final evaluation returning an in environment value
        
        Arguments:
            Environment environment:  holds the current environment variables
                           **kwargs:  any arguments the Evaluable requires to evaluate
        """
        
        raise Exception('eval(environment) not implemented')



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
            raise Exception(f'Variable {self.name} not found')
        
        return environment[self.name]
    
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f"Variable({self.name})"



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