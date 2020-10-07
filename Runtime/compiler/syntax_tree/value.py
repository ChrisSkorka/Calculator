from compiler.constants import *
from compiler.tokens_definition import *
from compiler.syntax_tree.token_node_builder import SyntaxTreeTokenNodeBuilder



class ValueSTTNB(SyntaxTreeTokenNodeBuilder):

    def __init__(self, token):
        super().__init__(token, 1)
        
    def isComplete(self):
        return True
   