#Input: Tokenizers (keywords, characters, etc)
#Output: Non-terminal and terminal language elements (In xxx.xml, with "xxx" is the name of .jack file)

#Notes for writing this program:
#   -For elements that appears 0 or more times, use while loop, after each time done processing that element
#   -For elements that appears 0 or 1 time, add that default element for them, then adding something or nothing, depends on the code
#   -Change the add_tags() method in tokenizer.py module to process a module
#   -Updated: add_tags(top, sub_element_ls): return new sub element added to the tree
# Current problem: expressionList and parameterList, must be printed in 2 lines (start and end tag) when they are empty, otherwise, print them normally

import JackTokenizer
import xml.etree.ElementTree as ET  #XML Element tree
from xml.dom import minidom     #XML DOM
import re

classVarDec = ['static', 'field']
statement_header = {'let':'CompileLet', 'if':'CompileIf', 'while':'CompileWhile', 'do':'CompileDo', 'return':'CompileReturn'}
op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
keyword_constants = ['true', 'false', 'null', 'this']
unary_op = ['~', '-']
subroutine = ['(', '.']

debug = ""

class Parser:
    def __init__(self, code):
        self.obj = JackTokenizer.Tokenizer(code)     #Token input, a list of elements
        self.top = self.CompileClass(self.obj)
        self.xml = ET.tostring(self.top, encoding='unicode')
        self.xml = minidom.parseString(self.xml)
        self.xml = self.xml.toprettyxml()
        self.xml = re.sub('<\?xml .*\?>\n', '', self.xml)
        self.xml = ET.tostring(ET.fromstring(self.xml), short_empty_elements=False).decode('utf-8')

    """Compile a class"""
    def CompileClass(self, obj):
        token_ls = obj.tokens       #List of non-terminal elements
        id = 0                      #token list tracker (For a class). In Jack language, there's only one class per file.
        top = ET.Element('class')
        sub = []                    #Sub elements of the tree
        for _ in range(3):          #Add keyword 'class', className and character '{'
            id, sub = obj.add_tags(token_ls[id], top, sub, id)

        while token_ls[id] in classVarDec and token_ls[id] != '}':
            id, sub = self.CompileClassVarDec(id, top, obj, sub)

        while token_ls[id] != '}':
            id, sub = self.CompileSubroutineDec(id, top, obj, sub)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)
        return top
    
    """Compile all class variables declaration, return the current index of token list"""
    def CompileClassVarDec(self, id, old_top, obj, sub):
        token_ls = obj.tokens 
        top = ET.SubElement(old_top, 'classVarDec')
        sub.append(top)

        for _ in range(3):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)
            
        while token_ls[id] == ',':
            for _ in range(2):
                id, sub = obj.add_tags(token_ls[id], top, sub, id)
            
        id, sub = obj.add_tags(token_ls[id], top, sub, id)
        return id, sub

    """Compile a subroutine (Or a function, method, etc)"""
    def CompileSubroutineDec(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'subroutineDec')
        sub.append(top)

        for _ in range(4):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)
        
        id, sub = self.CompileParameterList(id, top, obj, sub)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)

        id, sub = self.CompileSubroutineBody(id, top, obj, sub)
        return id, sub
    
    def CompileSubroutineBody(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'subroutineBody')
        sub.append(top)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)

        while token_ls[id] == 'var':
            id, sub = self.CompileVarDec(id, top, obj, sub)
        while token_ls[id] != '}':
            id, sub = self.CompileStatements(id, top, obj, sub)
        
        id, sub = obj.add_tags(token_ls[id], top, sub, id)
        return id, sub

    """Compile parameter list of a function (or method, etc)"""
    def CompileParameterList(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'parameterList')
        sub.append(top)

        if token_ls[id] != ')':
            for _ in range(2):
                id, sub = obj.add_tags(token_ls[id], top, sub, id)
        
            while token_ls[id] == ',':
                for _ in range(3):
                    id, sub = obj.add_tags(token_ls[id], top, sub, id)

        return id, sub
    
    def CompileVarDec(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'varDec')
        sub.append(top)

        for _ in range(3):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)
        while token_ls[id] == ',':
            for _ in range(2):
                id, sub = obj.add_tags(token_ls[id], top, sub, id)
        
        id, sub = obj.add_tags(token_ls[id], top, sub, id)

        return id, sub
    
    def CompileStatements(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'statements')
        sub.append(top)

        while token_ls[id] in statement_header:
            id, sub = getattr(self, statement_header[token_ls[id]])(id, top, obj, sub)
        return id, sub

    def CompileDo(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'doStatement')
        sub.append(top)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)
        
        while token_ls[id] != ';':
            id, sub = self.CompileSubroutineCall(id, top, obj, sub)
        
        id, sub = obj.add_tags(token_ls[id], top, sub, id)
        return id, sub

    def CompileLet(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'letStatement')
        sub.append(top)

        for _ in range(2):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)
        
        if token_ls[id] == '[':
            id, sub = obj.add_tags(token_ls[id], top, sub, id)

            id, sub = self.CompileExpression(id, top, obj, sub)
            
            id, sub = obj.add_tags(token_ls[id], top, sub, id)
        id, sub = obj.add_tags(token_ls[id], top, sub, id)

        id, sub = self.CompileExpression(id, top, obj, sub)
        
        id, sub = obj.add_tags(token_ls[id], top, sub, id)
        return id, sub

    def CompileWhile(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'whileStatement')
        sub.append(top)

        for _ in range(2):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)

        id, sub = self.CompileExpression(id, top, obj, sub)

        for _ in range(2):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)
        
        id, sub = self.CompileStatements(id, top, obj, sub)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)
        return id, sub

    def CompileReturn(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'returnStatement')
        sub.append(top)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)

        if token_ls[id] != ';':
            id, sub = self.CompileExpression(id, top, obj, sub)
        
        id, sub = obj.add_tags(token_ls[id], top, sub, id)
        return id, sub

    def CompileIf(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'ifStatement')
        sub.append(top)

        for _ in range(2):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)

        id, sub = self.CompileExpression(id, top, obj, sub)

        for _ in range(2):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)
        
        id, sub = self.CompileStatements(id, top, obj, sub)
        
        id, sub = obj.add_tags(token_ls[id], top, sub, id)
        
        if token_ls[id] == 'else':
            for _ in range(2):
                id, sub = obj.add_tags(token_ls[id], top, sub, id)
            
            id, sub = self.CompileStatements(id, top, obj, sub)

            id, sub = obj.add_tags(token_ls[id], top, sub, id)
        return id, sub

    def CompileExpression(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'expression')
        sub.append(top)

        id, sub = self.CompileTerm(id, top, obj, sub)

        while token_ls[id] in op:
            id, sub = obj.add_tags(token_ls[id], top, sub, id)
            id, sub = self.CompileTerm(id, top, obj, sub)
        
        return id, sub

    def CompileTerm(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'term')
        sub.append(top)

        if token_ls[id+1] in subroutine and obj.tag_type(token_ls[id]) == 'identifier':
            id, sub = self.CompileSubroutineCall(id, top, obj, sub)
        else:
            id, sub = obj.add_tags(token_ls[id], top, sub, id)
            
            if token_ls[id] == '[':     #expression case with varName at the beginning
                id, sub = obj.add_tags(token_ls[id], top, sub, id)
                while token_ls[id] != ']':
                    id, sub = self.CompileExpression(id, top, obj, sub)
                id, sub = obj.add_tags(token_ls[id], top, sub, id)
                
            elif token_ls[id-1] == '(':   #another expression case
                while token_ls[id] != ')':
                    id, sub = self.CompileExpression(id, top, obj, sub)
                id, sub = obj.add_tags(token_ls[id], top, sub, id)
                
            elif token_ls[id-1] in unary_op:
                id, sub = self.CompileTerm(id, top, obj, sub)
                
        return id, sub

    def CompileSubroutineCall(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = old_top
        while True:
            id, sub = obj.add_tags(token_ls[id], top, sub, id)
            if token_ls[id-1] == '(':
                break 
        
        #Handle expressionList
        id, sub = self.CompileExpressionList(id, top, obj, sub)

        #Handle ")"
        id, sub = obj.add_tags(token_ls[id], top, sub, id)
        return id, sub

    def CompileExpressionList(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'expressionList')
        sub.append(top)
        if token_ls[id] != ')':
            id, sub = self.CompileExpression(id, top, obj, sub)

        while token_ls[id] != ')':
            id, sub = obj.add_tags(token_ls[id], top, sub, id)
            id, sub = self.CompileExpression(id, top, obj, sub)
        
        return id, sub