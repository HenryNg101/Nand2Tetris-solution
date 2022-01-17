#This module is responsible for processing functions

push_data = "\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"

#Handling command "function f k"
def function_declaration(func_name, local_vars):
    local_vars = int(local_vars)
    ret = "(" + func_name + ")"
    while local_vars > 0:
        ret += "\n@SP\nA=M\nM=0\n@SP\nM=M+1\n"
        local_vars -= 1
    return ret

#Handling command "call f n"
def function_call(func_name, args, ret_add):
    result = "@" + ret_add + push_data.replace('M','A',1) + "@LCL" + push_data + "@ARG" + push_data + "@THIS" + push_data + "@THAT" + push_data
    result += "@SP\nD=M\n@LCL\nM=D\n@ARG\n"
    args = int(args)
    while args > 0:
        result += "D=D-1\n"
        args -= 1
    for _ in range(5):
        result += "D=D-1\n"
    result += ("M=D\n@" + func_name + "\n0;JMP\n" + "(" + ret_add + ")\n")
    return result

#Handling command "return" in a function
#Load the return address first, then the value later.
def return_value():
    update_segments = ["THAT","THIS","ARG","LCL","RET"]
    result = "@SP\nA=M-1\nD=M\n@RETVAL\nM=D\n@LCL\nD=M\n@FRAME\nM=D\n@ARG\n"
    result += "D=M\n@SP\nM=D+1\n@FRAME\nD=M\n"
    for segment in update_segments:
        result += ("@" + segment + "\nM=D-1\nA=M\nD=M\n@" + segment + "\nM=D\n@FRAME\nMD=M-1\n")
    result += "@RETVAL\nD=M\n@SP\nA=M-1\nM=D\n@RET\nA=M;JMP\n"
    return result