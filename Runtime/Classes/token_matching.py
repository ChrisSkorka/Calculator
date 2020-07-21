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