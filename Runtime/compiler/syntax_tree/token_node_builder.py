

class TokenNodeBuilder:

    def acceptsKeyword(self, string):
        return False

class ValueTokenNodeBuilder(TokenNodeBuilder):
    pass

class InfixOperatorTokenNodeBuilder(TokenNodeBuilder):
    pass

class PrefixOperatorTokenNodeBuilder(TokenNodeBuilder):
    pass

class PostfixOperatorTokenNodeBuilder(TokenNodeBuilder):
    pass

class GroupTokenNodeBuilder(TokenNodeBuilder):
    pass

class ReturnTokenNodeBuilder(TokenNodeBuilder):
    pass

class IfElseTokenNodeBuilder(TokenNodeBuilder):
    pass

class ForElseTokenNodeBuilder(TokenNodeBuilder):
    pass

class WhileTokenNodeBuilder(TokenNodeBuilder):
    pass

class SwitchTokenNodeBuilder(TokenNodeBuilder):
    pass

class FunctionTokenNodeBuilder(TokenNodeBuilder):
    pass

class ClassTokenNodeBuilder(TokenNodeBuilder):
    pass

class SignalTokenNodeBuilder(TokenNodeBuilder):
    pass