import sys

in_file = open(sys.argv[1], "r")
out_file = open(sys.argv[1].replace(".vm", ".asm"), "w")

code_data = in_file.read().split("\n")

for line in code_data:
    line = line.strip()
    if len(line) > 0:
        if line[0:2] != "//":
            out_file.write(line + "\n")     
abc 