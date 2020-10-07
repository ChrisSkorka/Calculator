from compiler.constants import *
from compiler.tokens_definition import *
from compiler.syntax_tree.group import GroupSTTNB
from compiler.syntax_tree.syntax_signal import SyntaxSignalSTTNB
from compiler.syntax_tree.value import ValueSTTNB
from compiler.syntax_tree.prefix_operator import PrefixOperatorSTTNB
from compiler.syntax_tree.infix_operator import InfixOperatorSTTNB



class ItemListSTTNB(GroupSTTNB):

    def bubbleUpAdd(self, current_child, new_child):

        if self.open:

            if type(new_child) == SyntaxSignalSTTNB:
                if new_child.token['function'] == 'newline':
                    return self
                
                elif new_child.token['function'] == 'comma':
                    self.addChild(new_child)
                    return self

                elif self.token['function'] == new_child.token['function']:
                    self.open = False
                    return self
                
                else:
                    raise Exception('Group not closed')
            
            else:
                self.insertChild(current_child, new_child)
                return new_child
        
        else:

            if type(new_child) in [
                    PrefixOperatorSTTNB, 
                    ValueSTTNB,
                    ItemListSTTNB,
                ]:

                call = InfixOperatorSTTNB(call_token)
                self.bubbleUpAddByPrecedence(current_child, call)
                call.addChild(new_child)

                return new_child
                
        return self.parent.bubbleUpAdd(self, new_child)
