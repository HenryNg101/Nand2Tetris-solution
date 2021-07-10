#In Hack Assembly, valid operations are: A+B, A-B, A&B, A|B, !A (Or !B), -A(Or -B)

two_operands_ops = {"add":"+", "sub":"-","and":"&","or":"|"}
one_operands_ops = {"neg":"-", "not":"!"}
compare_ops = {"eq":["JEQ","JNE"], "gt":["JGT","JLE"], "lt":["JLT","JGE"]}

def process(operation):
    if operation in tuple(two_operands_ops):
        return "\n@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M" + two_operands_ops[operation] + "D\n@SP\nM=M+1\n"
    else:
        return "\n@SP\nM=M-1\nA=M\nM=" + one_operands_ops[operation] + "M\n@SP\nM=M+1\n"

#Process comparison operations
def compare_process(operation, num):
    true = "@true" + str(num) 
    false = "@false" + str(num)
    jump = "@jump" + str(num)
    true_section = true.replace("@","(") + ")\nD=-1\n" + jump + "\n0;JMP\n"
    false_section = false.replace("@","(") + ")\nD=0\n" + jump + "\n0;JMP\n"
    jump_section = jump.replace("@","(") + ")\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
    return "\n@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nD=M-D\n" + true + "\nD;" + compare_ops[operation][0] + "\n" + false + "\nD;" + compare_ops[operation][1] + "\n" + true_section + false_section + jump_section