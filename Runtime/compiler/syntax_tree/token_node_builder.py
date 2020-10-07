from compiler.constants import *
from compiler.tokens_definition import *



class SyntaxTreeTokenNodeBuilder:

    def __init__(self, token, max_child_count=None):
        self.parent = None
        self.token = token
        self.children = []
        self.max_child_count = max_child_count
    
    def addChild(self, child):

        if self.max_child_count != None and len(self.children) >= self.max_child_count:
            print('addChild max', self, child)
            raise Exception(f'{type(self)} can have at most {self.max_child_count} children')
            
        self.children.append(child)
        child.parent = self

        self.onChildInserted(None, child)
        child.onAdded(self)

    def replaceChild(self, current_child, new_child):

        i = self.children.index(current_child)
        self.children[i] = new_child
        
        current_child.parent = None
        new_child.parent = self

        self.onChildInserted(current_child, new_child)
        current_child.onRemoved(self)
        new_child.onInserted(self)

    def insertChild(self, current_child, new_child):

        if current_child == None:
            self.addChild(new_child)
        else:
            self.replaceChild(current_child, new_child)
            new_child.addChild(current_child)

    def removeChild(self, child):

        self.children.remove(child)
        child.onRemoved(self)
    
    def onChildInserted(self, old_child, new_child):
        pass

    def onAdded(self, new_parent):
        pass

    def onInserted(self, new_parent):
        pass

    def onRemoved(self, old_parent):
        pass

    def isComplete(self):
        raise Exception(f'STTNB.isComplete() not implemented for type {type(self)}')

    def insertParent(self, parent):
        self.parent.replaceChild(self, parent)
        parent.addChild(self)

    def bubbleUpAdd(self, current_child, new_child):
        return self.bubbleUpAddByPrecedence(current_child, new_child)

    def bubbleUpAddByPrecedence(self, current_child, new_child):

        if (new_child.token['associativity'] == LEFT_ASSOCIATIVE
            and self.token['precedence'] <  new_child.token['precedence'] or 
            new_child.token['associativity'] == RIGHT_ASSOCIATIVE 
            and self.token['precedence'] <= new_child.token['precedence'] ):

            self.insertChild(current_child, new_child)
            return new_child

        else:
            return self.parent.bubbleUpAdd(self, new_child)

    def __repr__(self):
        return str(self)

    def __str__(self):
        name = f'{self.__class__.__name__}"{self.token["symbol"]}"'.replace('STTNB', '')
        args = ''  if len(self.children)==0 else f'( {", ".join(str(c) for c in self.children)} )'
        return name + args

class ValueSTTNB(SyntaxTreeTokenNodeBuilder):

    def __init__(self, token):
        super().__init__(token, 1)
        
    def isComplete(self):
        return True
        


class InfixOperatorSTTNB(SyntaxTreeTokenNodeBuilder):

    def __init__(self, token):
        super().__init__(token, 2)
        
    def isComplete(self):
        return len(self.children) == 2

class PrefixOperatorSTTNB(SyntaxTreeTokenNodeBuilder):

    def __init__(self, token):
        super().__init__(token, 1)
        
    def isComplete(self):
        return len(self.children) == 1

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



class GroupSTTNB(SyntaxTreeTokenNodeBuilder):
    
    def __init__(self, token):
        super().__init__(token, None)
        self.open = True

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

class ReferenceCodePairSTTNB(GroupSTTNB):
    pass

class ValueCodePairSTTNB(GroupSTTNB):
    pass

class CodeSTTNB(GroupSTTNB):
    pass

class ReturnSTTNB(GroupSTTNB):
    pass



class SyntaxSignalSTTNB(SyntaxTreeTokenNodeBuilder):
    pass



class ChainSTTNB(SyntaxTreeTokenNodeBuilder):
    pass

class ChainComparitorSTTNB(ChainSTTNB):
    pass