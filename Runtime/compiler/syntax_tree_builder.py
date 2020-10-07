from compiler.syntax_tree import *
import compiler.tokens_definition as tokens_definition



class SyntaxTreeBuilder:
    def __init__(self):
        code_block_toke = [g for g in tokens_definition.infix_operators if g['function'] == 'colon'][0]
        self.root = CodeBlockSTTNB(code_block_toke)
        self.focus = self.root
        
    def parseLine(self, tokens):
        
        for token in tokens:

            token_node_builder = token['builder'](token)
            # print('parseLine', 'focus =', self.focus, self.focus.token['precedence'], '|', 'new =', token_node_builder, token_node_builder.token['precedence'])
            self.focus = self.focus.bubbleUpAdd(None, token_node_builder)
            # print(self.focus)
