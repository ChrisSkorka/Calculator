from compiler.constants import *
from compiler.tokens_definition import *
from compiler.syntax_tree.token_node_builder import SyntaxTreeTokenNodeBuilder



class PostfixOperatorSTTNB(SyntaxTreeTokenNodeBuilder):

    def __init__(self, token):
        super().__init__(token, 1)
        
    def isComplete(self):
        return len(self.children) == 1

    def bubbleUpAdd(self, current_child, new_child):

        if self.isComplete():

            return self.parent.bubbleUpAdd(current_child, new_child)

            # if type(new_child) in [
            #         PrefixOperatorSTTNB, 
            #         ValueSTTNB,
            #         ItemListSTTNB,
            #     ]:

            #     call = InfixOperatorSTTNB(call_token)
            #     self.parent.bubbleUpAdd(current_child, call)
            #     call.addChild(new_child)

            #     return new_child
                
        # return self.parent.bubbleUpAdd(self, new_child)
        return self.bubbleUpAddByPrecedence(current_child, new_child)
