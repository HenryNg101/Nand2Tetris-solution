# Input: .jack file
# Output: Tokens of terminal elements (Input for parser)

import re   #regular expression. Link for testing any regular expression: https://pythex.org/
import xml.etree.ElementTree as ET  #XML Element tree
from xml.dom import minidom     #XML DOM

keyword = ["class", "constructor", "function", "method", "field", "static", "var", "int",
            "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if",
            "else", "while", "return"]

symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>',
            '=', '~']

class Tokenizer:
    def __init__(self, code):
        self.tokens = self.clean_code(code)
        #self.tokens = self.add_tags(self.tokens)
        #self.tokens = re.sub('<\?xml .*\?>\n', '', self.tokens)   #Remove prolog at the beginning

    """Clean comments (multi-line and single-line comments), newline and some spaces, and split to get all tokens"""

    def clean_code(self, code):
        # Clean single-line comments
        code = re.sub('//.*', '', code)
        # Clean multi-line comments
        code = re.sub('/\*.*?\*/', '', code, flags=re.DOTALL)
        # 2 problems with this code
        # String processing, and symbols processing
        code = code.replace('\n', ' ').strip()
        code = code.replace('\t', ' ')
        return self.seperate_tokens(code)

    """Seperate tokens in the code"""
    def seperate_tokens(self, data):
        tokens = []
        id = 0
        while id < len(data):
            # If it's a string, concatenate until the end of string (including space)
            if data[id] == '"':
                string = data[id]
                id += 1
                while data[id] != '"':
                    string += data[id]
                    id += 1
                string += data[id]
                id += 1
                tokens.append(string)
            # If it's not a string, concatenate until there is a whitespace or a symbol (except the first character is the symbol itself)
            elif data[id] != ' ':
                string = data[id]
                id += 1
                if string not in symbol:
                    while data[id] != ' ' and data[id] not in symbol:
                        string += data[id]
                        id += 1
                tokens.append(string)
            else:
                id += 1
        return tokens

    """Add a sub XML tags for the parent XML"""
    def add_tags(self, token, top, sub):     
        if token in keyword:
            sub.append(ET.SubElement(top, 'keyword'))
            sub[-1].text = token

        elif token in symbol:
            sub.append(ET.SubElement(top, 'symbol'))
            sub[-1].text = token

        elif token.isnumeric():
            sub.append(ET.SubElement(top, 'integerConstant'))
            sub[-1].text = token
            
        elif token[0] == '"':
            sub.append(ET.SubElement(top, 'stringConstant'))
            sub[-1].text = token.replace('"', ' ')

        else:
            sub.append(ET.SubElement(top, 'identifier'))
            sub[-1].text = token

        return sub

        #Beautify XML
        #result = ET.tostring(top, encoding='unicode')
        #reparsed = minidom.parseString(result)
        #return reparsed.toprettyxml()