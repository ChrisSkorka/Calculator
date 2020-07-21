from tokens import *
from Classes.token_tree_nodes import *


def re_match_length(string, re_pattern):
    match = re.match(re_pattern, string)
    return match.span()[1] if match != None else 0



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

def lexing(string, ans_available=False):
    tokens = []

    i = 0
    while i < len(string):
        
        if string[i] in ' ':
            i += 1
            continue
            
        last_token_type = tokens[-1][0] if len(tokens) > 0 else None
        allowed_token_types = []
        allowed_token_types_with_implicit_op = {}
        allowed_token_types_with_ans = {}

        # begin with
        if last_token_type in [
            None,
        ]:
            
            allowed_token_types = [TOKEN_TYPE_BINARY] if ans_available else []
            allowed_token_types += [
                TOKEN_TYPE_UNARY_LEFT,
                TOKEN_TYPE_OPEN_GROUP,
                TOKEN_TYPE_NEW_ITEM,
                TOKEN_TYPE_CLOSE_GROUP,
                *TOKEN_TYPE_VALUE,
            ]
            if ans_available:
                allowed_token_types_with_ans = {
                    TOKEN_TYPE_UNARY_RIGHT: '',
                    TOKEN_TYPE_BINARY: '',
                }
        
        if last_token_type in [\
            TOKEN_TYPE_OPEN_GROUP,
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
                    tokens.append((TOKEN_TYPE_LITERAL, implicit_op))
                elif implicit_op != None:
                    tokens.append((TOKEN_TYPE_BINARY, implicit_op))
                
                token_type = possible_token_type
                token_str = string[i:i+l]
                break
                

                    
        # invalid token
        if token_type == None:
            raise Exception(f"Token not allowed at position {i}")
            i += 1
        else:
            tokens.append((token_type, token_str))
            i += len(token_str)

    return tokens
