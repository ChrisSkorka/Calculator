# from Classes.evaluable_tree_nodes import *
from Classes.token_tree_nodes import *
from tokens import *



def bubble_up(focus, new):
    """
    Finds ancestor/parent in tree upwards from `token` thats the first group token or the first
    """
    
    while True:
#         print('bubble_up', focus.value, type(focus))
#         if type(focus) != NodeValue and (type(focus) == NodeGroup or focus.precedence < new.precedence):
        if type(focus) == NodeGroup or focus.precedence < new.precedence:
#             print('return', focus.value)
            return focus
        else:
            focus = focus.parent



def bubble_up_to_group(focus):
    while True:
        if type(focus) == NodeGroup:
            return focus
        else:
            focus = focus.parent



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

def build_token_tree(tokens):
    
    root = NodeGroup(find_token_definition('{', TOKEN_TYPE_OPEN_GROUP, lambda x:x.open_token), None)
    focus = root
    
    for token_type, value in tokens:
        
        
        # focus is
        # Binary Operator
        # Left Unary Operator
        if type(focus) in [
            NodeBinary,
            NodeUnaryLeft,
        ]:
            
            # next is 
            # Unary left
            if token_type == TOKEN_TYPE_UNARY_LEFT:
#                 print('insert lef unary')
                
                operand = find_token_definition(value, TOKEN_TYPE_UNARY_LEFT)
                next_node = NodeUnaryLeft(operand)
                
                focus.set_right(next_node)
                focus = next_node
                
            # next is
            # Group
            elif token_type == TOKEN_TYPE_OPEN_GROUP:
#                 print('insert open group')
                
                group = find_token_definition(value, TOKEN_TYPE_OPEN_GROUP, lambda x:x.open_token)
                next_node = NodeGroup(group)
                focus.set_right(next_node)
                focus = next_node
            
            # next is
            # TOKEN_TYPE_STRING
            # TOKEN_TYPE_INTEGER
            # TOKEN_TYPE_NUMBER
            # TOKEN_TYPE_LITERAL
            elif token_type in TOKEN_TYPE_VALUE:
#                 print('insert value')
                
                next_node = NodeValue(value, token_type)
                focus.set_right(next_node)
                focus = next_node
                
            else:
                raise Exception(f"token '{value}' not allowed here")
            
            
        # focus is
        # Value
        # Closed Group
        elif type(focus) == NodeValue or (type(focus) == NodeGroup and focus.is_complete()):
            
            # next is
            # Binary
            if token_type == TOKEN_TYPE_BINARY:
#                 print('insert binary')
                
                operand = find_token_definition(value, TOKEN_TYPE_BINARY)
                next_node = NodeBinary(operand)
                    
                parent_node = bubble_up(focus.parent, next_node)
                child_node = parent_node.get_right()
                parent_node.set_right(next_node)
                next_node.set_left(child_node)
                focus = next_node
                
            
            # next is
            # Unary right
            elif token_type == TOKEN_TYPE_UNARY_RIGHT:
#                 print('insert right unary')
                
                operand = find_token_definition(value, TOKEN_TYPE_UNARY_RIGHT)
                next_node = NodeUnaryRight(operand)
                    
                parent_node = focus.parent # bubble_up(focus.parent, next_node)
                child_node = parent_node.get_right()
                parent_node.set_right(next_node)
                next_node.set_left(child_node)
                # focus = next_node
            
            # next is
            # New item
            elif token_type == TOKEN_TYPE_NEW_ITEM:
#                 print('new item')
                
                token_definition = find_token_definition(value, TOKEN_TYPE_NEW_ITEM)
    
                parent_node = bubble_up_to_group(focus.parent)
                
                if token_definition.token in parent_node.group_definition.seperators:
                    
                    depth = parent_node.group_definition.seperators[token_definition.token]
                    if depth > 0:
                        parent_node.increase(depth)
                        focus = parent_node
                else:
                    raise Exception(f"token '{value}' not allowed here")
                    
            
            # next is
            # Close group
            elif token_type == TOKEN_TYPE_CLOSE_GROUP:
#                 print('close group')
                
                parent_node = bubble_up_to_group(focus.parent)
                parent_node.close()
                focus = parent_node
            
            # next is
            else:
                raise Exception(f"token '{value}' not allowed here")
#                 print('start new item in parent group')
        
        
        # focus is
        # Open Group
        elif type(focus) == NodeGroup and not focus.is_complete(): 
            
            # next is
            # Binary - use ans on left
            if token_type == TOKEN_TYPE_BINARY:
#                 print('insert binary with ans as left')

                left = NodeValue('ans', TOKEN_TYPE_LITERAL)
                
                operand = find_token_definition(value, TOKEN_TYPE_BINARY)
                next_node = NodeBinary(operand)
                next_node.set_left(left)
                
                focus.add(next_node)
                focus = next_node
            
            # next is
            # Unary left
            elif token_type == TOKEN_TYPE_UNARY_LEFT:
#                 print('add unary left')
                
                operand = find_token_definition(value, TOKEN_TYPE_UNARY_LEFT)
                next_node = NodeUnaryLeft(operand)
                
                focus.add(next_node)
                focus = next_node
            
            # next is
            # Group
            elif token_type == TOKEN_TYPE_OPEN_GROUP:
#                 print('add open group')
                
                group = find_token_definition(value, TOKEN_TYPE_OPEN_GROUP, lambda x:x.open_token)
                next_node = NodeGroup(group)
                focus.add(next_node)
                focus = next_node
            
            # next is
            # Close Group
            elif token_type == TOKEN_TYPE_CLOSE_GROUP:
#                 print('close group')
                
                focus.close()
            
            # next is
            # TOKEN_TYPE_STRING
            # TOKEN_TYPE_INTEGER
            # TOKEN_TYPE_NUMBER
            # TOKEN_TYPE_LITERAL
            elif token_type in TOKEN_TYPE_VALUE:
#                 print('add value')
                
                next_node = NodeValue(value, token_type)
                focus.add(next_node)
                focus = next_node
                
            # next is 
            # TOKEN_TYPE_NEW_ITEM
            elif token_type == TOKEN_TYPE_NEW_ITEM:
#                 print('new item/dimension')
                
                token_definition = find_token_definition(value, TOKEN_TYPE_NEW_ITEM)
                
                if token_definition.token in focus.group_definition.seperators:
                    
                    depth = focus.group_definition.seperators[token_definition.token]
                    if depth > 0:
                        focus.increase(depth)
                else:
                    raise Exception(f"token '{value}' not allowed here")
                
            # next is
            else:
                raise Exception(f"token '{value}' not allowed here")
#                 print('start new item in parent group')
            
        
    
    return root
    