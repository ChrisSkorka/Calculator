from compiler.tokenize import Tokenizer
from compiler.token_matcher import token_matchers
import compiler.tokens
from compiler.syntax_tree_builder import SyntaxTreeBuilder

try:
    tokenizer = Tokenizer()



    # tokenizer.tokenizeBlock("""\
    # function g(a,b,c:(?,2) = [1,2,,]):
    # 	x = a * b + c
    # 	return x
    # """)
    # tokenizer.tokenizeBlock("""\
    # 1 + + 2! * +-3  \
    # """)
    tokenizer.tokenizeBlock("""\
    function g(a,b,c:(?,2) = [1,2,,]):
        x = a * b + c
        return x
    a, b, c = 1,2,[3,4,,5,6]
    x = g(a,b,c)
    y = if x > 0: x else y
    print(y)
    """)


except Exception as e:
    print(e)

print([[t['function'],t['symbol']] for t in tokenizer.tokens])

try:
    syntax_tree_builder = SyntaxTreeBuilder()


    syntax_tree_builder.parseLine(tokenizer.tokens)

except Exception as e:
    print(e)



print(syntax_tree_builder.root)