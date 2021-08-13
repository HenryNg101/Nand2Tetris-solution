import JackTokenizer
import SymbolTable
import VMWriter

classVarDec = ['static', 'field']
statement_header = {'let':'CompileLet', 'if':'CompileIf', 'while':'CompileWhile', 'do':'CompileDo', 'return':'CompileReturn'}
op = ['+', '-', '*', '/', '&', '|', '<', '>', '=']
keyword_constants = ['true', 'false', 'null', 'this']
unary_op = {'~':'not', '-':'neg'}
subroutine = ['(', '.']

class Parser:
    def __init__(self, code, classname):
        self.obj = JackTokenizer.Tokenizer(code)     #Token input, a list of elements
        self.code = ""
        self.code = self.CompileClass(self.obj, self.code, classname)

    """Compile the whole class"""
    def CompileClass(self, obj, code, classname):
        token_ls = obj.tokens
        classTable = SymbolTable.Table()
        funcTable = SymbolTable.Table()
        id = 3
        while token_ls[id] in classVarDec and token_ls[id] != '}':
            id, classTable = self.CompileClassVarDec(id, obj, classTable)
    
        while token_ls[id] != '}':
            id, sub, code = self.CompileSubroutineDec(id, obj, sub, classname, classTable, funcTable, code)

        return code

    """Add class variables to class symbol table"""
    def CompileClassVarDec(self, id, obj, table):
        token_ls = obj.tokens
        var_kind = token_ls[id]
        var_type = token_ls[id+1]
        var_name = token_ls[id+2]
        table.define(var_name, var_type, var_kind)          #Add the first variable
        id += 3
        while token_ls[id] == ',':                          #Add more variable goes by the ',' character (if there's any)
            var_name = token_ls[id+1]
            table.define(var_name, var_type, var_kind)
            id += 2

        id += 1
        return id, table

    def CompileSubroutineDec(self, id, obj, className, classTable, funcTable, code):
        token_ls = obj.tokens
        func_type = token_ls[id]                            #Difference between constructor, function and method: 
        return_type = token_ls[id+1]
        func_name = token_ls[id+2]
        id += 4
        funcTable.startSubroutine()

        id, funcTable = self.CompileParameterList(id, obj, funcTable)

        id += 1

        id, code = self.CompileSubroutineBody(id, obj, className, classTable, func_name, return_type, func_type, funcTable, code)
        return id

    def CompileSubroutineBody(self, id, obj, className, classTable, func_name, return_type, func_type, funcTable, code):
        token_ls = obj.tokens
        id += 1

        while token_ls[id] == "var":
            id, funcTable = self.CompileVarDec(id, obj, funcTable)
        
        code += VMWriter.writeFunction(className + "." + func_name, funcTable.varcount('local'))
        if func_type == 'method':                          #Normal method (Just for method, not for function)
            funcTable.define("this", className, 'argument')
            code += VMWriter.writePush('argument', 0)           #For a method, the this pointer must point to the 1st argument
            code += VMWriter.writePop('pointer', 0)

        elif func_type == 'constructor':
            code += VMWriter.writePush('constant', classTable.varcount('field'))
            code += VMWriter.writeCall('Memory.alloc', 1)       #Memory.alloc(n) returns the base address of created object => load into THIS segment
            code += VMWriter.writePop('pointer', 0)

        while token_ls[id] != '}':
            id, code = self.CompileStatements(id, obj, classTable, funcTable, return_type, code)
        
        id += 1
        return id, code

    def CompileParameterList(self, id, obj, table):
        token_ls = obj.tokens

        if token_ls[id] != ')':
            arg_type = token_ls[id]
            arg_name = token_ls[id+1]
            table.define(arg_name, arg_type, 'argument')
            id += 2

            while token_ls[id] == ',':
                arg_type = token_ls[id+1]
                arg_name = token_ls[id+2]
                table.define(arg_name, arg_type, 'argument')
                id += 3
        
        return id, table

    def CompileVarDec(self, id, obj, funcTable):
        token_ls = obj.tokens
        var_type = token_ls[id+1]
        var_name = token_ls[id+2]
        funcTable.define(var_name, var_type, 'local')
        id += 3

        while token_ls[id] == ',':
            var_name = token_ls[id+1]
            funcTable.define(var_name, var_type, 'local')
            id += 2

        id += 1
        return id, funcTable

    def CompileStatements(self, id, obj, classTable, funcTable, return_type, code):
        token_ls = obj.tokens

        while token_ls[id] in statement_header:
            id, code = getattr(self, statement_header[token_ls[id]])(id, obj, classTable, funcTable, return_type, code)
        
        return id, code

    def CompileDo(self, id, obj, classTable, funcTable, return_type, code):
        pass

    def CompileLet(self, id, obj, classTable, funcTable, return_type, code):
        pass

    def CompileWhile(self, id, obj, classTable, funcTable, return_type, code):
        pass

    def CompileReturn(self, id, obj, classTable, funcTable, return_type, code):
        pass

    def CompileIf(self, id, obj, classTable, funcTable, return_type, code):
        pass

    def CompileExpression(self, id, obj, classTable, funcTable, code):         
        #To handle expression (term (op term)*), we compile the first term first, then the next operator and term together.
        #Eg: x + y * z => Compile x, then compile "+ y", then "* z".
        token_ls = obj.tokens
        id, code = self.CompileTerm(id, obj, classTable, funcTable, code)
        
        while token_ls[id] in op:
            id, code = self.CompileTerm(id, obj, classTable, funcTable, code)
            #Then, code += smt, to add the operator (add, sub, neg, etc)
        
        return id, code

    def CompileTerm(self, id, obj, classTable, funcTable, code):
        token_ls = obj.tokens

        if obj.tag_type(token_ls[id]) == 'integerConstant':
            code += VMWriter.writePush('constant', token_ls[id])

        elif obj.tag_type(token_ls[id]) == 'stringConstant':
            code += VMWriter.writePush('constant', len(token_ls[id]))
            code += VMWriter.writeCall('String.new', 1)
            for char in token_ls[id]:
                code += VMWriter.writePush('constant', ord(char))
                code += VMWriter.writeCall('String.appendChar', 2)

        elif token_ls[id] in keyword_constants:
            if token_ls[id] == 'this':
                code += VMWriter.writePush('pointer', 0)
            elif token_ls[id] == 'true':
                code += VMWriter.writePush('constant', 0)
                code += VMWriter.writeArithmetic('not')
            else:
                code += VMWriter.writePush('constant', 0)       # false and null case.

        elif token_ls[id] in unary_op:                          # unaryOp term
            arithmetic = token_ls[id]
            id, code = self.CompileTerm(id, obj, classTable, funcTable, code)
            code += VMWriter.writeArithmetic(unary_op[arithmetic])
        
        elif token_ls[id] == '(':                               # '(' expression ')'
            id += 1
            while token_ls[id] != ')':
                id, code = self.CompileExpression(id, obj, classTable, funcTable, code)
            id += 1
        
        elif classTable.kindof(token_ls[id]) == None:           # subroutineCall
            id, code = self.CompileSubroutineCall(id, obj, classTable, funcTable, code)
        
        else:                                                   # varName and varName '[' expression ']'
            var_name = token_ls[id]
            segment = funcTable.kindof(var_name) if funcTable.kindof(var_name) != None else classTable.kindof(var_name)
            value = funcTable.indexof(var_name) if funcTable.indexof(var_name) != None else classTable.indexof(var_name)
            code += VMWriter.writePush(segment, value)
            if token_ls[id+1] == '[':
                id += 1
                while token_ls[id] != ']':
                    id, code = self.CompileExpression(id, obj, classTable, funcTable, code)
                id += 1
                code += VMWriter.writeArithmetic('add')

        return id, code

    def CompileSubroutineCall(self, id, obj, classTable, funcTable, code):
        token_ls = obj.tokens
        func_name = token_ls[id]

    def CompileExpressionList(self, id, old_top, obj, sub):
        pass