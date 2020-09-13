from compiler.abstract_syntax_tree import *
import compiler.tokens as tokens


class SyntaxTreeBuilder:
    def __init__(self):
        self.root = None
        self.focus = CodeBlockTokenNodeBuilder()
        
    def parseLine(self, tokens):
        
        for token in tokens:
            
            if isinstance(self.focus, CodeBlockTokenNodeBuilder):
                
                if token['syntax_type'] == tokens.KEYWORD:
                    pass
                if token['syntax_type'] == tokens.VALUE:
                    pass
                if token['syntax_type'] == tokens.INFIX:
                    pass
                if token['syntax_type'] == tokens.PREFIX:
                    pass
                if token['syntax_type'] == tokens.POSTFIX:
                    pass
                if token['syntax_type'] == tokens.SEPERATORS:
                    pass
                if token['syntax_type'] == tokens.GROUP_OPEN:
                    pass
                if token['syntax_type'] == tokens.GROUP_CLOSE:
                    pass


            if isinstance(self.focus, ValueTokenNodeBuilder):
                
                if token['syntax_type'] == tokens.KEYWORD:
                    pass
                if token['syntax_type'] == tokens.VALUE:
                    pass
                if token['syntax_type'] == tokens.INFIX:
                    pass
                if token['syntax_type'] == tokens.PREFIX:
                    pass
                if token['syntax_type'] == tokens.POSTFIX:
                    pass
                if token['syntax_type'] == tokens.SEPERATORS:
                    pass
                if token['syntax_type'] == tokens.GROUP_OPEN:
                    pass
                if token['syntax_type'] == tokens.GROUP_CLOSE:
                    pass


            if isinstance(self.focus, InfixOperatorTokenNodeBuilder):
                
                if token['syntax_type'] == tokens.KEYWORD:
                    pass
                if token['syntax_type'] == tokens.VALUE:
                    pass
                if token['syntax_type'] == tokens.INFIX:
                    pass
                if token['syntax_type'] == tokens.PREFIX:
                    pass
                if token['syntax_type'] == tokens.POSTFIX:
                    pass
                if token['syntax_type'] == tokens.SEPERATORS:
                    pass
                if token['syntax_type'] == tokens.GROUP_OPEN:
                    pass
                if token['syntax_type'] == tokens.GROUP_CLOSE:
                    pass


            if isinstance(self.focus, PrefixOperatorTokenNodeBuilder):
                
                if token['syntax_type'] == tokens.KEYWORD:
                    pass
                if token['syntax_type'] == tokens.VALUE:
                    pass
                if token['syntax_type'] == tokens.INFIX:
                    pass
                if token['syntax_type'] == tokens.PREFIX:
                    pass
                if token['syntax_type'] == tokens.POSTFIX:
                    pass
                if token['syntax_type'] == tokens.SEPERATORS:
                    pass
                if token['syntax_type'] == tokens.GROUP_OPEN:
                    pass
                if token['syntax_type'] == tokens.GROUP_CLOSE:
                    pass


            if isinstance(self.focus, PostfixOperatorTokenNodeBuilder):
                
                if token['syntax_type'] == tokens.KEYWORD:
                    pass
                if token['syntax_type'] == tokens.VALUE:
                    pass
                if token['syntax_type'] == tokens.INFIX:
                    pass
                if token['syntax_type'] == tokens.PREFIX:
                    pass
                if token['syntax_type'] == tokens.POSTFIX:
                    pass
                if token['syntax_type'] == tokens.SEPERATORS:
                    pass
                if token['syntax_type'] == tokens.GROUP_OPEN:
                    pass
                if token['syntax_type'] == tokens.GROUP_CLOSE:
                    pass


            if isinstance(self.focus, SyntaxConstructTokenNodeBuilder):
                
                if token['syntax_type'] == tokens.KEYWORD:
                    pass
                if token['syntax_type'] == tokens.VALUE:
                    pass
                if token['syntax_type'] == tokens.INFIX:
                    pass
                if token['syntax_type'] == tokens.PREFIX:
                    pass
                if token['syntax_type'] == tokens.POSTFIX:
                    pass
                if token['syntax_type'] == tokens.SEPERATORS:
                    pass
                if token['syntax_type'] == tokens.GROUP_OPEN:
                    pass
                if token['syntax_type'] == tokens.GROUP_CLOSE:
                    pass


            if isinstance(self.focus, SyntaxVerticalSignalTokenNodeBuilder):
                
                if token['syntax_type'] == tokens.KEYWORD:
                    pass
                if token['syntax_type'] == tokens.VALUE:
                    pass
                if token['syntax_type'] == tokens.INFIX:
                    pass
                if token['syntax_type'] == tokens.PREFIX:
                    pass
                if token['syntax_type'] == tokens.POSTFIX:
                    pass
                if token['syntax_type'] == tokens.SEPERATORS:
                    pass
                if token['syntax_type'] == tokens.GROUP_OPEN:
                    pass
                if token['syntax_type'] == tokens.GROUP_CLOSE:
                    pass


            if isinstance(self.focus, SyntaxHorizontalSignalTokenNodeBuilder):
                
                if token['syntax_type'] == tokens.KEYWORD:
                    pass
                if token['syntax_type'] == tokens.VALUE:
                    pass
                if token['syntax_type'] == tokens.INFIX:
                    pass
                if token['syntax_type'] == tokens.PREFIX:
                    pass
                if token['syntax_type'] == tokens.POSTFIX:
                    pass
                if token['syntax_type'] == tokens.SEPERATORS:
                    pass
                if token['syntax_type'] == tokens.GROUP_OPEN:
                    pass
                if token['syntax_type'] == tokens.GROUP_CLOSE:
                    pass


