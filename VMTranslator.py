import sys
import operations
import memory
import branching
import function
import pathlib

in_name = sys.argv[1]
code_data = []
out_file = ""

if in_name[-3:len(in_name)] == '.vm':   #When user want to translate a .vm file
    in_file = open(sys.argv[1], "r")
    file_name = sys.argv[1].split('/')[-1].replace('.vm','')
    out_file = open(sys.argv[1].replace(".vm", ".asm"), "w")
    code_data = in_file.read().split("\n")

else:                                   #When user want to translate a whole directory
    directory = pathlib.Path(in_name).glob("*.vm")
    out_file = open(in_name + "/" + in_name.split('/')[-1] + '.asm', 'w')
    for vm_file in directory:
        code = open(vm_file, 'r')
        code = code.read().split('\n')
        code_data.extend(code)

file_name = in_name.split('/')[-1]
actual_code = []
compare_tracking = 0
return_tracking = 0

#filtering comments and lines with no character.
for line in code_data:
    line = line.strip()
    if len(line) > 0:
        if line[0:2] != "//":
            line = line.split("//")[0].strip()
            actual_code.append(line)

#Bootstrap code
#out_file.write("@256\nD=A\n@SP\nM=D\n")
#out_file.write(function.function_call("Sys.init", "0", "ret" + str(return_tracking)))
#return_tracking += 1
out_file.write("@Sys.init\n0;JMP\n")
#out_file.write("@ret0\n" + function.push_data.replace('M', 'A', 1) + "@LCL" + function.push_data + "@ARG" + function.push_data + "@THIS" + function.push_data + "@THAT" + function.push_data)
#out_file.write("M=D\n@Sys.init\n0;JMP\n(ret0)\n")

for line in actual_code:
    line = line.split(" ")
    if len(line) == 1:
        if line[0] in tuple(operations.compare_ops):
            line = operations.compare_process(line[0], compare_tracking)
            compare_tracking += 1
        elif line[0] != "return":
            line = operations.process(line[0])
        else:
            line = function.return_value()
    elif len(line) == 2:
        label_types = {'label':'label_processing','goto':'unconditional_jump','if-goto':'conditional_jump'}
        line = getattr(branching, label_types[line[0]])(line[1])
    elif len(line) == 3:
        if line[1] not in ['local', 'argument', 'this', 'that'] and line[0] in ['push', 'pop']:
            if line[1] == "static":
                line = memory.static(line[0], line[2], file_name)
            elif line[1] == "constant":
                line = memory.constant(line[2])
            else:
                line = getattr(memory, line[1])(line[0], line[2])
        elif line[0] not in ["call", "function"]:
            line = memory.normal_type(line[0],line[1],line[2])
        else:
            if line[0] == "call":
                line = function.function_call(line[1], line[2], "ret" + str(return_tracking))
                return_tracking += 1
            else:
                line = function.function_declaration(line[1], line[2])
    out_file.write(line)
out_file.write("(END_LOOP)\n@END_LOOP\n0;JMP")