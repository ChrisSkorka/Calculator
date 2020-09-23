from compiler.tokenize import Tokenizer
from compiler.token_matcher import token_matchers
import compiler.tokens_definition
from compiler.syntax_tree_builder import SyntaxTreeBuilder

try:
    tokenizer = Tokenizer()



    tokenizer.tokenizeBlock("""\
g = function (a,b,c: [1,2,,]):
    x = a * b! + c
    return x
y = g(1, 2, 3)
""")
    # tokenizer.tokenizeBlock("""\
# 1 + + 2! * +-3  \
    # """)
#     tokenizer.tokenizeBlock("""\
# function g(a,b,c = [1,2,,]):
#     x = a * b + c
#     return x
# a, b, c = 1,2,[3,4,,5,6]
# x = g(a,b,c)
# y = if x > 0: x else y
# print(y)
#     """)
#     tokenizer.tokenizeBlock("""\
# fun_gen arg1 arg2 arg3 \
#     """)
#     tokenizer.tokenizeBlock("""\
# fun_gen arg1! arg2 arg3 \
#     """)
#     tokenizer.tokenizeBlock("""\
# ((fun_gen arg1) arg2) arg3 \
#     """)


except KeyboardInterrupt as e:
    print(e)

print( [ ([t['function'],t['symbol']] + ([t['indent']] if 'indent' in t else [])) for t in tokenizer.tokens])
print()



try:

    syntax_tree_builder = SyntaxTreeBuilder()

    syntax_tree_builder.parseLine(tokenizer.tokens)

except KeyboardInterrupt as e:
    print(syntax_tree_builder.root)
    raise e



print(syntax_tree_builder.root)
# print('')
# print(vars(syntax_tree_builder.root.children[0].children[1].children[0]))