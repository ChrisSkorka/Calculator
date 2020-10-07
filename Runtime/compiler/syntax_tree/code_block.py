from compiler.constants import *
from compiler.tokens_definition import *
from compiler.syntax_tree.group import GroupSTTNB
from compiler.syntax_tree.syntax_signal import SyntaxSignalSTTNB



class CodeBlockSTTNB(GroupSTTNB):
    
    def __init__(self, token):
        super().__init__(token)
        self.depth = None
        self.has_left = False

    def bubbleUpAdd(self, current_child, new_child):

        if self.open:

            if type(new_child) == SyntaxSignalSTTNB:

                if new_child.token['function'] == 'newline':

                    if self.has_left and len(self.children) == 1   or   len(self.children) == 0:
                        self.depth = new_child.token['indent']
                        return self

                    elif new_child.token['indent'] == self.depth:
                        return self

                    elif self.depth == None   or   new_child.token['indent'] < self.depth:
                        self.open = False
                        return self.parent.bubbleUpAdd(current_child, new_child)

                    else:
                        raise Exception('Unexpected level of indent')
                
                elif self.depth != None and new_child.token['function'] == 'semi_column':
                    return self
                
                else:
                    self.open = False
                    return self.parent.bubbleUpAdd(current_child, new_child)
            
            else:
                self.insertChild(current_child, new_child)
                return new_child

        return self.parent.bubbleUpAdd(self, new_child)

    def onInserted(self, new_parent):
        self.has_left = True
