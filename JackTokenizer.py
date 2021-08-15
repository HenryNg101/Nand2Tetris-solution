# Input: .jack file
# Output: Tokens of terminal elements (Input for parser)

import re   #regular expression. Link for testing any regular expression: https://pythex.org/
import xml.etree.ElementTree as ET  #XML Element tree

keyword = ["class", "constructor", "function", "method", "field", "static", "var", "int",
            "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if",
            "else", "while", "return"]

symbol = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>',
            '=', '~']

class Tokenizer:
    def __init__(self, code):
        self.tokens = self.clean_code(code)

    """Clean comments (multi-line and single-line comments), newline and some spaces, and split to get all tokens"""
    def clean_code(self, code):
        # Clean single-line comments
        code = re.sub('//.*', '', code)
        # Clean multi-line comments
        code = re.sub('/\*.*?\*/', '', code, flags=re.DOTALL)
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

    """Decide the type of token passed to the function"""
    def tag_type(self, token):
        #Boolean list for checking all conditions to decide which is the type of a token 
        bool_ls = [token in keyword, token in symbol, token.isnumeric(), token[0] == '"']
        bool_ls.append(not (bool_ls[0] or bool_ls[1] or bool_ls[2] or bool_ls[3]))
        #Return result with same index 
        result_ls = ['keyword', 'symbol', 'integerConstant', 'stringConstant', 'identifier']
        return result_ls[bool_ls.index(True)]

    """Add a sub XML tags for the parent XML"""
    def add_tags(self, token, top, sub, id):
        sub.append(ET.SubElement(top, self.tag_type(token)))
        token = token.replace('"', '')  #Just in case it's a stringConstant
        sub[-1].text = token
        return id+1, sub