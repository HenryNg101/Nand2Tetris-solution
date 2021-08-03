#This module is used to emits VM commands, using the VM command syntax

class Writer:
    def __init__(self, file_name):
        self.class_name = file_name

    """The main function to write VM, this function call other function"""
    def generate_code(self, top):
        #First, take the class name (For function name, etc)
        #Then, process class variable declaration (until there's no variable to process)
        #Then, process methods:
        #- For each methods, process method parameters (if there's any)
        #- Then, process expressions. For each expression, check if there's any expression inside expression, if yes, call appropriate function to process that expression, and so on.
        pass

    def writePush(self):
        pass

    def writePop(self):
        pass

    def writeArithmetic(self):
        pass

    def writeLabel(self):
        pass

    def writeGoto(self):
        pass

    def writeIf(self):
        pass

    def writeCall(self):
        pass

    def writeFunction(self):
        pass

    def writeReturn(self):
        pass