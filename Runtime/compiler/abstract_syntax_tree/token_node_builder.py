

class TokenNodeBuilder:

    # def __init__(self):
    #     self.children = []
    
    def addChild(self, builder):
        raise Exception(f'TokenNodeBuilder.addChild() not implemented for type {type(self)}')

    def isComplete(self, builder):
        raise Exception(f'TokenNodeBuilder.isComplete() not implemented for type {type(self)}')

class ValueTokenNodeBuilder(TokenNodeBuilder):

    def __init__(self, token):
        self.token = token
        self.child = None
    
    def addChild(self, builder):

        if self.child == None:
            self.child = builder
        else:
            raise Exception('Cannot add multimple children to ValueTokenNodeBuilder')
        
    def isComplete(self, builder):
        return True

class InfixOperatorTokenNodeBuilder(TokenNodeBuilder):

    def __init__(self, token):
        self.token = token
        self.children = []
    
    def addChild(self, builder):

        if len(self.children) >= 2:
            self.children.append(builder)
        else:
            raise Exception('Cannot add more than 2 children to InfixOperatorTokenNodeBuilder')
        
    def isComplete(self, builder):
        return len(self.children) == 2

class PrefixOperatorTokenNodeBuilder(TokenNodeBuilder):

    def __init__(self, token):
        self.token = token
        self.child = None
    
    def addChild(self, builder):

        if self.child == None:
            self.child = builder
        else:
            raise Exception('Cannot add multimple children to ValueTokenNodeBuilder')
        
    def isComplete(self, builder):
        return not self.child == None

class PostfixOperatorTokenNodeBuilder(TokenNodeBuilder):

    def __init__(self, token):
        self.token = token
        self.child = None
    
    def addChild(self, builder):

        if self.child == None:
            self.child = builder
        else:
            raise Exception('Cannot add multimple children to ValueTokenNodeBuilder')
        
    def isComplete(self, builder):
        return not self.child == None



class SyntaxConstructTokenNodeBuilder(TokenNodeBuilder):

    def verticalSignal(self, string):
        return False

    def horizontalSignal(self, string):
        return False

class CodeBlockTokenNodeBuilder(SyntaxConstructTokenNodeBuilder):
    
    def __init__(self):
        self.depth = None

class GroupTokenNodeBuilder(SyntaxConstructTokenNodeBuilder):
    pass

class IfTokenNodeBuilder(SyntaxConstructTokenNodeBuilder):
    pass

class ForTokenNodeBuilder(SyntaxConstructTokenNodeBuilder):
    pass

class WhileTokenNodeBuilder(SyntaxConstructTokenNodeBuilder):
    pass

class SwitchTokenNodeBuilder(SyntaxConstructTokenNodeBuilder):
    pass

class FunctionTokenNodeBuilder(SyntaxConstructTokenNodeBuilder):
    pass

class ClassTokenNodeBuilder(SyntaxConstructTokenNodeBuilder):
    pass

class ReturnTokenNodeBuilder(SyntaxConstructTokenNodeBuilder):
    pass



class SyntaxVerticalSignalTokenNodeBuilder(TokenNodeBuilder):
    pass

class SyntaxHorizontalSignalTokenNodeBuilder(TokenNodeBuilder):
    pass



class ChainTokenNodeBuilder(TokenNodeBuilder):
    pass

class ChainComparitorTokenNodeBuilder(ChainTokenNodeBuilder):
    pass