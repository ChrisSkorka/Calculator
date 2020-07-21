from Classes.token_matching import *

class BuiltIns():
    
    def __init__(self):
        self.functions = []
        self.function_parameter_evaluation_parameters = {}
        self.vars = []
        self.binary_operators = []
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
        
    def register_binary_operator(self, name, precedence):
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