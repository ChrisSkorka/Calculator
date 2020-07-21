import re
from Classes.built_ins import built_ins



# Tokens Types
TOKEN_TYPE_STRING =   'string'
TOKEN_TYPE_INTEGER =  'integer'
TOKEN_TYPE_NUMBER =   'number'
TOKEN_TYPE_OPERATOR = 'operand'
TOKEN_TYPE_OPEN_GROUP = 'group'
TOKEN_TYPE_LITERAL =  'literal'

TOKEN_TYPE_OPEN_GROUP = 'open group'
TOKEN_TYPE_CLOSE_GROUP = 'close group'
TOKEN_TYPE_NEW_ITEM    = 'new item'
TOKEN_TYPE_BINARY      = 'binary operand'
TOKEN_TYPE_UNARY_LEFT  = 'left unary operand'
TOKEN_TYPE_UNARY_RIGHT = 'right unary operand'

OPERAND_TYPES = [
    TOKEN_TYPE_OPEN_GROUP,
    TOKEN_TYPE_CLOSE_GROUP, 
    TOKEN_TYPE_NEW_ITEM, 
    TOKEN_TYPE_BINARY, 
    TOKEN_TYPE_UNARY_LEFT, 
    TOKEN_TYPE_UNARY_RIGHT, 
]

TOKEN_TYPE_VALUE = [
    TOKEN_TYPE_STRING,
    TOKEN_TYPE_INTEGER,
    TOKEN_TYPE_NUMBER,
    TOKEN_TYPE_LITERAL,
]



# Token Operations
token_definitions = {
    TOKEN_TYPE_OPEN_GROUP:  built_ins.groups,
    TOKEN_TYPE_CLOSE_GROUP: built_ins.groups, 
    TOKEN_TYPE_NEW_ITEM:    built_ins.new_items, 
    TOKEN_TYPE_BINARY:      built_ins.binary_operators, 
    TOKEN_TYPE_UNARY_LEFT:  built_ins.left_unary_operators, 
    TOKEN_TYPE_UNARY_RIGHT: built_ins.right_unary_operators, 
}



# Operation Indexing
def find_token_definition(string, token_type, f = lambda x:x.token):
    for token_definition in token_definitions[token_type]:
        if string == f(token_definition):
#         if re.fullmatch(operator.re_match, string) != None:
            return token_definition
    return None



# Define Token Regular Expressions
def re_join(l, f=lambda x:x):
    items = [f(i) for i in l]
    items.sort(key=lambda x:len(x), reverse=True)
    return '(' + ')|('.join([re.escape(i) for i in items]) + ')'

# regex
re_number =    r"""((([\.][0-9]+)|([0-9]+[\.]?[0-9]*))([eE][-+]?[0-9]+)?)"""
re_integer =   r"""((0b|0o|0d|0x|[0-9]+_)[0-9a-zA-Z,]+)"""
re_string =    r"""((\""".*?\""")|('''.*?''')|(".*?")|('.*?'))"""
re_literal =   r"""([A-Za-z_][A-Za-z0-9_]*)"""


re_open_group =           re_join(built_ins.groups, lambda x:x.open_token)
re_close_group =          re_join(built_ins.groups, lambda x:x.close_token)
re_binary_operands =      re_join(built_ins.binary_operators, lambda x:x.token)
re_left_unary_operands =  re_join(built_ins.left_unary_operators, lambda x:x.token)
re_right_unary_operands = re_join(built_ins.right_unary_operators, lambda x:x.token)
re_new_item =             re_join(built_ins.new_items, lambda x:x.token)


re_tokens = {
    TOKEN_TYPE_STRING:      re_string,
    TOKEN_TYPE_INTEGER:     re_integer,
    TOKEN_TYPE_NUMBER:      re_number,
    TOKEN_TYPE_LITERAL:     re_literal,
    TOKEN_TYPE_OPEN_GROUP:  re_open_group,
    TOKEN_TYPE_BINARY:      re_binary_operands,
    TOKEN_TYPE_UNARY_LEFT:  re_left_unary_operands,
    TOKEN_TYPE_UNARY_RIGHT: re_right_unary_operands,
    TOKEN_TYPE_NEW_ITEM:    re_new_item,
    TOKEN_TYPE_CLOSE_GROUP: re_close_group,
}