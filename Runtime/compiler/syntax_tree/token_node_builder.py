from compiler.constants import LEFT_ASSOCIATIVE, RIGHT_ASSOCIATIVE
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
