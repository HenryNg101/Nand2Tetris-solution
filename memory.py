push_operation_general = "\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
pop_operation_general = "\n@SP\nM=M-1\nA=M\nD=M\n"
standard_segments = {'local':'LCL','argument':'ARG','this':'THIS','that':'THAT'}

#Process standard segments (defined above) (works well !!)
def normal_type(operation, segment, value):
    value = int(value)
    value1 = value
    segment = standard_segments[segment]
    if operation == "push":
        result = "\n@" + segment
        while value > 0:
            result += "\nM=M+1"
            value -= 1
        result += ("\nA=M\nD=M" + push_operation_general)
        if value1 > 0:
            result += ("\n@" + segment + "\n")
        while value1 > 0:
            result += "M=M-1\n"
            value1 -=1
    else:
        result = pop_operation_general + "\n@" + segment
        while value > 0:
            result += "\nM=M+1"
            value -=1
        result += ("\nA=M\nM=D")
        if value1 > 0:
            result += ("\n@" + segment + "\n")
        while value1 > 0:
            result += "M=M-1\n"
            value1 -=1
    return result

#Process constants (works well !!)
def constant(value):
    return "\n@" + value + "\nD=A\n" + push_operation_general + "\n"

#Process static segment (worked !!)
def static(operation, value, filename):
    if operation == "push":
        return "\n@" + filename + "." + str(value) + "\nD=M" + push_operation_general + "\n"
    else:
        return pop_operation_general + "@" + filename + "." + str(value) + "\nM=D\n"

#Process "temp" memory segment (works well !!)
def temp(operation, value):
    value = int(value)
    if operation == "push":
        result = "@5"
        while value > 0:
            result += "\nA=A+1"
            value -= 1
        result += ("\nD=M\n" + push_operation_general + "\n")
    else:
        result = pop_operation_general + "@5"
        while value > 0:
            result += "\nA=A+1"
            value -= 1
        result += "\nM=D\n"
    return result

#Process pointer segment (worked !!)
def pointer(operation, value):
    value = bool(int(value))
    segment = "THAT" if value else "THIS"
    if operation == "push":
        return "\n@" + segment + "\nD=M" + push_operation_general + "\n"
    else:
        return pop_operation_general + "@" + segment + "\nM=D\n"