#Input: Tokenizers (keywords, characters, etc)
#Output: Non-terminal and terminal language elements (In xxx.xml, with "xxx" is the name of .jack file)

#Notes for writing this program:
#   -For elements that appears 0 or more times, use while loop, after each time done processing that element
#   -For elements that appears 0 or 1 time, add that default element for them, then adding something or nothing, depends on the code
#   -Change the add_tags() method in tokenizer.py module to process a module
#   -Updated: add_tags(top, sub_element_ls): return new sub element added to the tree
#Currently working at CompileParameterList()


import tokenizer
import xml.etree.ElementTree as ET

classVarDec = ['static', 'field']

class Parser:
    def __init__(self, code):
        self.obj = tokenizer.Tokenizer(code)     #Token input, a list of elements
        self.xml = self.CompileClass(self.obj)

    """Compile a class"""
    def CompileClass(self, obj):
        token_ls = obj.tokens       #List of non-terminal elements
        id = 0                      #token list tracker
        top = ET.Element('class')
        sub = []                    #Sub elements of the tree
        for _ in range(3):          #Add keyword 'class', className and character '{'
            sub = obj.add_tags(token_ls[id], top, sub)
            id += 1

        while token_ls[id] != 'function' and token_ls[id] != '}':
            id, sub = self.CompileClassVarDec(id, top, obj, sub)

        while token_ls[id] != '}':
            id, sub = self.CompileSubroutine()

        sub = obj.add_tags(token_ls[id], top, sub)
        id += 1
        return top
    
    """Compile all class variables declaration, return the current index of token list"""
    def CompileClassVarDec(self, id, old_top, obj, sub):
        token_ls = obj.tokens 
        top = ET.SubElement(old_top, 'classVarDec')

        for _ in range(3):
            sub = obj.add_tags(token_ls[id], top, sub)
            id += 1
            
        while token_ls[id] == ',':
            for _ in range(2):
                sub = obj.add_tags(token_ls[id], top, sub)
                id += 1
            
        sub = obj.add_tags(token_ls[id], top, sub)
        id += 1
        return id, sub

    """Compile a subroutine (Or a function, method, etc)"""
    def CompileSubroutine(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'subroutineDec')
        for _ in range(4):
            sub = obj.add_tags(token_ls[id], top, sub)
            id += 1
        
        if token_ls[id] == ')':     #Default parameterList tag
            sub.append(ET.SubElement(top, 'parameterList'))
        else:
            while token_ls[id] != ')':
                id, sub = self.CompileParameterList(self, id, top, sub)
        for _ in range(2):
            sub = obj.add_tags(token_ls[id], top, sub)
            id += 1
        while token_ls[id] != '}':
            id, sub = self.CompileClassVarDec()

    """Compile parameter list of a function (or method, etc)"""
    def CompileParameterList(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'parameterList')
        for _ in range(2):
            sub = obj.add_tags(token_ls[id], top, sub)
            id += 1
        
        while token_ls[id] == ',':
            for _ in range(2):
                sub = obj.add_tags(token_ls[id], top, sub)
                id += 1

        return id, sub
    
    def CompileVarDec(self):
        pass
    
    def CompileStatements(self):
        pass

    def CompileDo(self):
        pass

    def CompileLet(self):
        pass

    def CompileWhile(self):
        pass

    def CompileReturn(self):
        pass

    def CompileIf(self):
        pass

    def CompileExpression(self):
        pass

    def CompileTerm(self):
        pass

    def CompileExpressionList(self):
        pass