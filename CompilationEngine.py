import JackTokenizer
import SymbolTable
import VMWriter

classVarDec = ['static', 'field']
statement_header = {'let':'CompileLet', 'if':'CompileIf', 'while':'CompileWhile', 'do':'CompileDo', 'return':'CompileReturn'}
op = {'+':'add', '-':'sub', '*':'Math.multiply', '/':'Math.divide', '&':'and', '|':'or', '<':'lt', '>':'gt', '=':'eq'}
keyword_constants = ['true', 'false', 'null', 'this']
unary_op = {'~':'not', '-':'neg'}
subroutine = ['(', '.']

class Parser:
    def __init__(self, code):
        self.obj = JackTokenizer.Tokenizer(code)     #Token input, a list of elements
        #print(self.obj.tokens)
        self.code = ""
        self.code = self.CompileClass(self.obj, self.code)

    """Compile the whole class"""
    def CompileClass(self, obj, code):
        token_ls = obj.tokens
        classTable = SymbolTable.Table()
        funcTable = SymbolTable.Table()
        classname = token_ls[1]
        id = 3
        while token_ls[id] in classVarDec and token_ls[id] != '}':
            id, classTable = self.CompileClassVarDec(id, obj, classTable)
    
        while token_ls[id] != '}':
            id, code = self.CompileSubroutineDec(id, obj, classname, classTable, funcTable, code)

        id += 1
        return code

    """Add class variables to class symbol table"""
    def CompileClassVarDec(self, id, obj, table):
        token_ls = obj.tokens
        var_kind = token_ls[id] if token_ls[id] != 'field' else 'this'
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
        func_name = token_ls[id+2]
        id += 4
        funcTable.startSubroutine()

        if func_type == 'method':
            funcTable.define("this", className, 'argument')
        id, funcTable = self.CompileParameterList(id, obj, funcTable)

        id += 1

        id, code = self.CompileSubroutineBody(id, obj, className, classTable, func_name, func_type, funcTable, code)
        return id, code

    def CompileSubroutineBody(self, id, obj, className, classTable, func_name, func_type, funcTable, code):
        token_ls = obj.tokens
        id += 1
        if_count = 0
        while_count = 0

        while token_ls[id] == "var":
            id, funcTable = self.CompileVarDec(id, obj, funcTable)
        
        code += VMWriter.writeFunction(className + "." + func_name, funcTable.varcount('local'))
        if func_type == 'method':                          #Normal method (Just for method, not for function)
            code += VMWriter.writePush('argument', 0)           #For a method, the this pointer must point to the 1st argument
            code += VMWriter.writePop('pointer', 0)

        elif func_type == 'constructor':
            code += VMWriter.writePush('constant', classTable.varcount('this'))
            code += VMWriter.writeCall('Memory.alloc', 1)       #Memory.alloc(n) returns the base address of created object => load into THIS segment
            code += VMWriter.writePop('pointer', 0)

        while token_ls[id] != '}':
            id, code, if_count, while_count = self.CompileStatements(id, obj, className, classTable, funcTable, code, if_count, while_count)
        
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

    def CompileStatements(self, id, obj, className, classTable, funcTable, code, if_count, while_count):
        token_ls = obj.tokens

        while token_ls[id] in statement_header:
            id, code, if_count, while_count = getattr(self, statement_header[token_ls[id]])(id, obj, className, classTable, funcTable, code, if_count, while_count)
        
        return id, code, if_count, while_count

    def CompileDo(self, id, obj, className, classTable, funcTable, code, if_count, while_count):
        token_ls = obj.tokens
        id += 1

        while token_ls[id] != ';':
            id, code = self.CompileSubroutineCall(id, obj, className, classTable, funcTable, code)
        
        code += VMWriter.writePop('temp', 0)
        id += 1
        return id, code, if_count, while_count

    def CompileLet(self, id, obj, className, classTable, funcTable, code, if_count, while_count):
        token_ls = obj.tokens
        var_name = token_ls[id+1]
        segment = funcTable.kindof(var_name) if funcTable.kindof(var_name) != None else classTable.kindof(var_name)
        value = funcTable.indexof(var_name) if funcTable.indexof(var_name) != None else classTable.indexof(var_name)
        id += 2
        is_array = token_ls[id] == '['

        if is_array:
            id += 1
            id, code = self.CompileExpression(id, obj, className, classTable, funcTable, code)
            code += VMWriter.writePush(segment, value)
            code += VMWriter.writeArithmetic('add')
            id += 1
        id += 1
        id, code = self.CompileExpression(id, obj, className, classTable, funcTable, code)
        if is_array:
            code += VMWriter.writePop('temp', 0)
            code += VMWriter.writePop('pointer', 1)
            code += VMWriter.writePush('temp', 0)
            code += VMWriter.writePop('that', 0)
        else:
            code += VMWriter.writePop(segment, value)
        id += 1
        return id, code, if_count, while_count

    def CompileWhile(self, id, obj, className, classTable, funcTable, code, if_count, while_count):
        lcl_while_count = while_count
        while_count += 1
        code += VMWriter.writeLabel("WHILE_EXP" + str(lcl_while_count))
        id += 2

        id, code = self.CompileExpression(id, obj, className, classTable, funcTable, code)
        code += VMWriter.writeArithmetic("not")
        code += VMWriter.writeIf('WHILE_END' + str(lcl_while_count))
        id += 2

        id, code, if_count, while_count = self.CompileStatements(id, obj, className, classTable, funcTable, code, if_count, while_count)
        code += VMWriter.writeGoto("WHILE_EXP" + str(lcl_while_count))
        code += VMWriter.writeLabel("WHILE_END" + str(lcl_while_count))
        id += 1

        return id, code, if_count, while_count

    def CompileReturn(self, id, obj, className, classTable, funcTable, code, if_count, while_count):
        token_ls = obj.tokens
        id += 1

        if token_ls[id] != ';':
            id, code = self.CompileExpression(id, obj, className, classTable, funcTable, code)
        else:
            code += VMWriter.writePush('constant', 0)
        
        code += VMWriter.writeReturn()
        id += 1
        return id, code, if_count, while_count

    def CompileIf(self, id, obj, className, classTable, funcTable, code, if_count, while_count):
        lcl_if_count = if_count
        if_count += 1
        token_ls = obj.tokens
        id += 2

        id, code = self.CompileExpression(id, obj, className, classTable, funcTable, code)
        id += 2

        code += VMWriter.writeIf('IF_TRUE' + str(lcl_if_count))
        code += VMWriter.writeGoto('IF_FALSE' + str(lcl_if_count))
        code += VMWriter.writeLabel('IF_TRUE' + str(lcl_if_count))

        id, code, if_count, while_count = self.CompileStatements(id, obj, className, classTable, funcTable, code, if_count, while_count)
        id += 1

        if token_ls[id] == 'else':
            #Handle the else case
            code += VMWriter.writeGoto('IF_END' + str(lcl_if_count))
            code += VMWriter.writeLabel('IF_FALSE' + str(lcl_if_count))
            id += 2

            id, code, if_count, while_count = self.CompileStatements(id, obj, className, classTable, funcTable, code, if_count, while_count)
            
            code += VMWriter.writeLabel('IF_END' + str(lcl_if_count))
            id += 1
        else:
            code += VMWriter.writeLabel('IF_FALSE' + str(lcl_if_count))
        
        return id, code, if_count, while_count

    def CompileExpression(self, id, obj, className, classTable, funcTable, code):         
        #To handle expression (term (op term)*), we compile the first term first, then the next operator and term together.
        #Eg: x + y * z => Compile x, then compile "+ y", then "* z".
        token_ls = obj.tokens
        id, code = self.CompileTerm(id, obj, className, classTable, funcTable, code)
        
        while token_ls[id] in op:
            operator = token_ls[id]
            id += 1
            id, code = self.CompileTerm(id, obj, className, classTable, funcTable, code)
            if "Math" not in op[operator]: 
                code += VMWriter.writeArithmetic(op[operator])          # Primitive type 
            else:
                code += VMWriter.writeCall(op[operator], 2)             # Class type
            #Then, code += smt, to add the operator (add, sub, neg, etc)
        
        return id, code

    def CompileTerm(self, id, obj, className, classTable, funcTable, code):
        token_ls = obj.tokens

        if obj.tag_type(token_ls[id]) == 'integerConstant':
            code += VMWriter.writePush('constant', token_ls[id])
            id += 1

        elif obj.tag_type(token_ls[id]) == 'stringConstant':
            token_ls[id] = token_ls[id].replace('"', '')
            code += VMWriter.writePush('constant', len(token_ls[id]))
            code += VMWriter.writeCall('String.new', 1)
            for char in token_ls[id]:
                code += VMWriter.writePush('constant', ord(char))
                code += VMWriter.writeCall('String.appendChar', 2)
            id += 1

        elif token_ls[id] in keyword_constants:
            if token_ls[id] == 'this':
                code += VMWriter.writePush('pointer', 0)
            elif token_ls[id] == 'true':
                code += VMWriter.writePush('constant', 0)
                code += VMWriter.writeArithmetic('not')
            else:
                code += VMWriter.writePush('constant', 0)       # false and null case.
            id += 1

        elif token_ls[id] in unary_op:                          # unaryOp term
            arithmetic = token_ls[id]
            id += 1
            id, code = self.CompileTerm(id, obj, className, classTable, funcTable, code)
            code += VMWriter.writeArithmetic(unary_op[arithmetic])
        
        elif token_ls[id] == '(':                               # '(' expression ')'
            id += 1
            while token_ls[id] != ')':
                id, code = self.CompileExpression(id, obj, className, classTable, funcTable, code)
            id += 1
        
        elif (classTable.kindof(token_ls[id]) == None and funcTable.kindof(token_ls[id]) == None) or token_ls[id+1] == '.':           # subroutineCall
            id, code = self.CompileSubroutineCall(id, obj, className, classTable, funcTable, code)
        
        else:                                                   # varName and varName '[' expression ']'
            var_name = token_ls[id]
            segment = funcTable.kindof(var_name) if funcTable.kindof(var_name) != None else classTable.kindof(var_name)
            value = funcTable.indexof(var_name) if funcTable.indexof(var_name) != None else classTable.indexof(var_name)
            id += 1
            if token_ls[id] == '[':
                id += 1
                while token_ls[id] != ']':
                    id, code = self.CompileExpression(id, obj, className, classTable, funcTable, code)
                id += 1
                code += VMWriter.writePush(segment, value)
                code += VMWriter.writeArithmetic('add')
                code += VMWriter.writePop('pointer', 1)
                code += VMWriter.writePush('that', 0)
            else:
                code += VMWriter.writePush(segment, value)

        return id, code

    # (Incomplete method)
    def CompileSubroutineCall(self, id, obj, className, classTable, funcTable, code):
        token_ls = obj.tokens
        func_name = ""
        args = 0
        if token_ls[id+1] != '.':
            func_name = className + '.' + token_ls[id]
            args += 1                                   #Add "this" argument (when called without specifying class name => call method)
            code += VMWriter.writePush('pointer', 0)
            id += 2
        else:
            func_name = token_ls[id+1] + token_ls[id+2]
            parent_class = funcTable.typeof(token_ls[id]) if funcTable.typeof(token_ls[id]) != None else classTable.typeof(token_ls[id])
            if parent_class != None:
                func_name = parent_class + func_name
                var_kind = funcTable.kindof(token_ls[id]) if funcTable.kindof(token_ls[id]) != None else classTable.kindof(token_ls[id])
                var_count = funcTable.indexof(token_ls[id]) if funcTable.indexof(token_ls[id]) != None else classTable.indexof(token_ls[id])
                args += 1
                code += VMWriter.writePush(var_kind, var_count)
            else:
                func_name = token_ls[id] + func_name

            id += 4

        id, code, args = self.CompileExpressionList(id, obj, className, classTable, funcTable, code, args)
        code += VMWriter.writeCall(func_name, args)
        id += 1
        return id, code

    def CompileExpressionList(self, id, obj, className, classTable, funcTable, code, args):
        token_ls = obj.tokens
        if token_ls[id] != ')':
            args += 1
            id, code = self.CompileExpression(id, obj, className, classTable, funcTable, code)

        while token_ls[id] != ')':
            args += 1
            id += 1
            id, code = self.CompileExpression(id, obj, className, classTable, funcTable, code)
        
        return id, code, args