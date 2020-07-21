from Classes.evaluable_tree_nodes import *
from Classes.data_types import *
from tokens import *



class NodeToken():
    """represents a value, operation or grouping node that returns an evaluabe that can be evaluated to return a value"""
    
    def is_complete(self):
        """Returns whether this token is complete, if false, it is not a valud token and interpreting failed"""
        
        raise Exception('is_complete() not implemented')
        
    def set_left(self, node):
        """sets the left child node if it exists"""
        
        raise Exception('set_left(node) not implemented')

    def set_right(self, node):
        """sets the right child node if it exists"""
        
        raise Exception('set_right(node) not implemented')
        
    def get_right(self):
        """segetsts the right child node if it exists"""
        
        raise Exception('get_right() not implemented')
        
    def get_evaluable(self):
        """return an Evaluable obejct from this token, the token should be complete before this method is called"""
        
        raise Exception('get_evaluable() not implemented')



class NodeBinary(NodeToken):
    """represents a binary operation with a left and right child"""
    
    def __init__(self, operation_definition, parent=None):
        self.parent = parent
        self.operation_definition = operation_definition
        self.precedence = operation_definition.precedence
        self.left = None
        self.right = None
    
    def is_complete(self):
        return self.left != None and self.right != None
        
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



class NodeUnaryLeft(NodeToken):
    """represents a unary operator to the left of its operand with a single child"""
    
    def __init__(self, operation_definition, parent=None):
        self.parent = parent
        self.operation_definition = operation_definition
        self.precedence = operation_definition.precedence
        self.child = None
    
    def is_complete(self):
        return self.child != None
        
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



class NodeUnaryRight(NodeToken):
    """represents a unary operator to the right of its operand with a single child"""
    
    def __init__(self, operation_definition, parent=None):
        self.parent = parent
        self.operation_definition = operation_definition
        self.precedence = operation_definition.precedence
        self.child = None
    
    def is_complete(self):
        return self.child != None
        
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



class NodeGroup(NodeToken):
    """represents a grouping"""
    
    def __init__(self, group_definition, parent=None):
        self.parent = parent
        self.children = []
        
        self.group_definition = group_definition
        self.complete = False
        
        self.shape = {}
        self.sep_count = 0
    
    def is_complete(self):
        return self.complete

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



