import sys
import operations
import memory

in_file = open(sys.argv[1], "r")
file_name = sys.argv[1].split('/')[-1].replace('.vm','')
out_file = open(sys.argv[1].replace(".vm", ".asm"), "w")

code_data = in_file.read().split("\n")
actual_code = []
tracking = 0

#filtering comments and lines with no character.
for line in code_data:
    line = line.strip()
    if len(line) > 0:
        if line[0:2] != "//":
            actual_code.append(line)

for line in actual_code:
    line = line.split(" ")
    if len(line) == 1:
        if line[0] in tuple(operations.compare_ops):
            line = operations.compare_process(line[0], tracking)
            tracking += 1
        else:
            line = operations.process(line[0])
    elif len(line) == 2:
        line = memory.constant(line[1])
    elif len(line) == 3:
        if line[1] not in ['local', 'argument', 'this', 'that']:
            if line[1] == "static":
                line = memory.static(line[0], line[2], file_name)
            elif line[1] == "constant":
                line = memory.constant(line[2])
            else:
                line = getattr(memory, line[1])(line[0], line[2])
        else:
            line = memory.normal_type(line[0],line[1],line[2])
    out_file.write(line)
out_file.write("(LOOP)\n@LOOP\n0;JMP")