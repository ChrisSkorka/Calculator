from compiler.tokenize import Tokenizer
from compiler.token_matcher import token_matchers
import compiler.tokens

# tokens = 
tokenizer = Tokenizer()

# tokenizer.tokenizeBlock("""\
# function g(a,b,c:(?,2) = [1,2,,]):
# 	x = a * b + c
# 	return x
# """)
tokenizer.tokenizeBlock("""\
1 + + 2! * +-3  \
""")




print([[t['function'],t['symbol']] for t in tokenizer.tokens])

# print(tokenizer.tokens)