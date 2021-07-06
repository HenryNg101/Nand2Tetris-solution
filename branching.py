def label_processing(label_name):
    return "\n(" + label_name + ")\n"

def unconditional_jump(label_name):     #Don't pop stack value, JMP
    return "\n@" + label_name + "\n0;JMP\n"

def conditional_jump(label_name):       #Pop stack value, then JNE
    return "\n@" + label_name + "\n@SP\nM=M-1\n@SP\nA=M\nD=M\n@" + label_name + "\nD;JNE\n"