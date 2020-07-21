from Classes.built_ins import built_ins
from Classes.data_structures import *
from Classes.data_types import *



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
        
    def addLn(self, ln):
        name = f'ln{self.ln_count}'
        self[name] = ln
        self[''] = ln
        
        self.ln_count += 1
        self.ans_available = True
        
        return name
    
    def enterScope(self, dictionary=None):
        return Environment(self, dictionary)
        
    def exitScope(self):
        return self if self.parent == None else self.parent
        
    def __repr__(self):
        return str(self)
    
    def __str__(self):
        return f'Environment({self.dictionary, self.parent})'



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