#This module is used to emits VM commands, using the VM command syntax

#push segment index => Push the value of segment[index] onto the stack
def writePush(segment, value):
    return "push " + segment + " " + str(value) + "\n"

#pop segment index Pop the top stack value and store it in segment[index].
def writePop(segment, value):
    return "pop " + segment + " " + str(value) + "\n"

def writeArithmetic(arithmetic):
    return arithmetic + "\n"

def writeLabel(label):
    return "label " + label + "\n"

def writeGoto(label):
    return "goto " + label + "\n"

def writeIf(label):
    return "if-goto " + label + "\n"

#Call a function after passed n arguments
def writeCall(func_name, args):
    return "call " + func_name + " " + str(args) +"\n"

#Write a function with n local variables
def writeFunction(func_name, vars):                   
    return "function " + func_name + " " + str(vars) + "\n"

def writeReturn():
    return "return\n"