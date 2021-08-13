#This module is used to emits VM commands, using the VM command syntax

def writePush(self, segment, value):
    return "push " + segment + " " + str(value) + "\n"

def writePop(self, segment, value):
    return "pop " + segment + " " + str(value) + "\n"

def writeArithmetic(self, arithmetic):
    return arithmetic + "\n"

def writeLabel(self, label):
    return "label " + label + "\n"

def writeGoto(self, label):
    return "goto " + label + "\n"

def writeIf(self, label):
    return "if-goto " + label + "\n"

#Call a function after passed n arguments
def writeCall(self, func_name, args):
    return "call " + func_name + " " + str(args) +"\n"

#Write a function with n local variables
def writeFunction(self, func_name, vars):                   
    return "function " + func_name + " " + str(vars) + "\n"

def writeReturn(self):
    return "return"