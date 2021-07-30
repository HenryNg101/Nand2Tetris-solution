#Input: Tokenizers (keywords, characters, etc)
#Output: Non-terminal and terminal language elements (In xxx.xml, with "xxx" is the name of .jack file)

# Notes for reading the code:
#   - Each method in the class is responsible for a non-terminal element 
#   - Each obj.add_tags() method is to add a terminal element. To know what element is added, each line has it's own comment about the element to be added
#   - Global lists and dictionary are used for checking purposes

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

class Parser:
    def __init__(self, code):
        self.obj = JackTokenizer.Tokenizer(code)     #Token input, a list of elements
        self.top = self.CompileClass(self.obj)
        self.xml = ET.tostring(self.top, encoding='unicode')
        #Make the XML result look good (with tab) using XML DOM Minidom
        self.xml = minidom.parseString(self.xml)
        self.xml = self.xml.toprettyxml()
        self.xml = re.sub('<\?xml .*\?>\n', '', self.xml)       #Remove XML prolog
        self.xml = ET.tostring(ET.fromstring(self.xml), short_empty_elements=False).decode('utf-8')

    def CompileClass(self, obj):
        token_ls = obj.tokens       #List of non-terminal elements
        id = 0                      #token list tracker (For a class). In Jack language, there's only one class per file.
        top = ET.Element('class')
        sub = []                    #Sub elements of the tree
        for _ in range(3):          
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # 'class', className and '{'

        while token_ls[id] in classVarDec and token_ls[id] != '}':
            id, sub = self.CompileClassVarDec(id, top, obj, sub)

        while token_ls[id] != '}':
            id, sub = self.CompileSubroutineDec(id, top, obj, sub)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # '}'
        return top
    
    def CompileClassVarDec(self, id, old_top, obj, sub):
        token_ls = obj.tokens 
        top = ET.SubElement(old_top, 'classVarDec')
        sub.append(top)

        for _ in range(3):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # 'static'|'field', type and varName
            
        while token_ls[id] == ',':
            for _ in range(2):
                id, sub = obj.add_tags(token_ls[id], top, sub, id)      # ',' and varName
            
        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # ';'
        return id, sub

    def CompileSubroutineDec(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'subroutineDec')
        sub.append(top)

        for _ in range(4):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # 'constructor'|'function'|'method', 'void'|type, subroutineName and '('
        
        id, sub = self.CompileParameterList(id, top, obj, sub)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # ')'

        id, sub = self.CompileSubroutineBody(id, top, obj, sub)
        return id, sub
    
    def CompileSubroutineBody(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'subroutineBody')
        sub.append(top)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # '{'

        while token_ls[id] == 'var':
            id, sub = self.CompileVarDec(id, top, obj, sub)
        while token_ls[id] != '}':
            id, sub = self.CompileStatements(id, top, obj, sub)
        
        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # '}'
        return id, sub

    def CompileParameterList(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'parameterList')
        sub.append(top)

        if token_ls[id] != ')':
            for _ in range(2):
                id, sub = obj.add_tags(token_ls[id], top, sub, id)      # type and varName
        
            while token_ls[id] == ',':
                for _ in range(3):
                    id, sub = obj.add_tags(token_ls[id], top, sub, id)  # ',', type and varName

        return id, sub
    
    def CompileVarDec(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'varDec')
        sub.append(top)

        for _ in range(3):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # 'var', type and varName
        while token_ls[id] == ',':
            for _ in range(2):
                id, sub = obj.add_tags(token_ls[id], top, sub, id)      # ',' and varName
        
        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # ';'

        return id, sub
    
    def CompileStatements(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'statements')
        sub.append(top)

        while token_ls[id] in statement_header:
            id, sub = getattr(self, statement_header[token_ls[id]])(id, top, obj, sub)  #Decide the type of statement to process
        return id, sub

    def CompileDo(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'doStatement')
        sub.append(top)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # 'do'
        
        while token_ls[id] != ';':
            id, sub = self.CompileSubroutineCall(id, top, obj, sub)
        
        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # ';'
        return id, sub

    def CompileLet(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'letStatement')
        sub.append(top)

        for _ in range(2):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # 'let' and varName
        
        if token_ls[id] == '[':
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # '['

            id, sub = self.CompileExpression(id, top, obj, sub)
            
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # ']'
        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # '='

        id, sub = self.CompileExpression(id, top, obj, sub)
        
        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # ';'
        return id, sub

    def CompileWhile(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'whileStatement')
        sub.append(top)

        for _ in range(2):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # 'while' and '('

        id, sub = self.CompileExpression(id, top, obj, sub)

        for _ in range(2):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # ')' and '{'
        
        id, sub = self.CompileStatements(id, top, obj, sub)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # '}'
        return id, sub

    def CompileReturn(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'returnStatement')
        sub.append(top)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # 'return'

        if token_ls[id] != ';':
            id, sub = self.CompileExpression(id, top, obj, sub)
        
        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # ';'
        return id, sub

    def CompileIf(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'ifStatement')
        sub.append(top)

        for _ in range(2):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # 'if' and '('

        id, sub = self.CompileExpression(id, top, obj, sub)

        for _ in range(2):
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # ')' and '{'
        
        id, sub = self.CompileStatements(id, top, obj, sub)
        
        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # '}'
        
        if token_ls[id] == 'else':
            for _ in range(2):
                id, sub = obj.add_tags(token_ls[id], top, sub, id)      # 'else' and '{'
            
            id, sub = self.CompileStatements(id, top, obj, sub)

            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # '}'
        return id, sub

    def CompileExpression(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'expression')
        sub.append(top)

        id, sub = self.CompileTerm(id, top, obj, sub)

        while token_ls[id] in op:
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # op
            id, sub = self.CompileTerm(id, top, obj, sub)
        
        return id, sub

    def CompileTerm(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'term')
        sub.append(top)

        if token_ls[id+1] in subroutine and obj.tag_type(token_ls[id]) == 'identifier':
            id, sub = self.CompileSubroutineCall(id, top, obj, sub)
        else:
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # varName | '(' | unaryOp 
            
            if token_ls[id] == '[':     #expression case with varName at the beginning
                id, sub = obj.add_tags(token_ls[id], top, sub, id)      # '['
                while token_ls[id] != ']':
                    id, sub = self.CompileExpression(id, top, obj, sub)
                id, sub = obj.add_tags(token_ls[id], top, sub, id)      # ']'
                
            elif token_ls[id-1] == '(':   #another expression case
                while token_ls[id] != ')':
                    id, sub = self.CompileExpression(id, top, obj, sub)
                id, sub = obj.add_tags(token_ls[id], top, sub, id)      # ')'
                
            elif token_ls[id-1] in unary_op:
                id, sub = self.CompileTerm(id, top, obj, sub)
                
        return id, sub

    def CompileSubroutineCall(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = old_top
        while True:
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # subroutineName and '(' | (className | varName), '.' and subroutineName 
            if token_ls[id-1] == '(':
                break 

        id, sub = self.CompileExpressionList(id, top, obj, sub)

        id, sub = obj.add_tags(token_ls[id], top, sub, id)              # ')'
        return id, sub

    def CompileExpressionList(self, id, old_top, obj, sub):
        token_ls = obj.tokens
        top = ET.SubElement(old_top, 'expressionList')
        sub.append(top)
        if token_ls[id] != ')':
            id, sub = self.CompileExpression(id, top, obj, sub)

        while token_ls[id] != ')':
            id, sub = obj.add_tags(token_ls[id], top, sub, id)          # ','
            id, sub = self.CompileExpression(id, top, obj, sub)
        
        return id, sub