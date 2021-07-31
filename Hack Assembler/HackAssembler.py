import sys

def a_instructions_processing(line):
    line = line[1:len(line)]
    if line in predefined_symbols:
        line = predefined_symbols[line]
    elif line in label_symbols:
        line = label_symbols[line]
    elif line in variable_symbols:
        line = variable_symbols[line]
    else:
        line = int(line)
    line = str(bin(line)).replace('0b', '')
    while len(line) < 16:
        line = '0' + line
    line += '\n'
    return line

def seperate_instruction_fields(line):
    dest = ""
    jump = ""
    comp = ""
    if '=' in line:
        dest = line.split('=')[0]
        if ';' in line:
            jump = line.split(';')[1]
            comp = line.split('=')[1].split(';')[0]
        else:
            comp = line.split('=')[1]
    else:
        if ';' in line:
            comp = line.split(';')[0]
            jump = line.split(';')[1]
    return [comp, dest, jump]

def computation_processing(comp):
    processed_comp = str(int('M' in comp))
    if 'M' in comp:
        comp = comp.replace('M','A')
    comp_dict = {'':'000000'
                ,'0':'101010'
                ,'1':'111111'
                ,'-1':'111010'
                ,'D':'001100'
                ,'A':'110000'
                ,'!D':'001101'
                ,'!A':'110001'
                ,'-D':'001111'
                ,'-A':'110011'
                ,'D+1':'011111'
                ,'A+1':'110111'
                ,'D-1':'001110'
                ,'A-1':'110010'
                ,'D+A':'000010'
                ,'D-A':'010011'
                ,'A-D':'000111'
                ,'D&A':'000000'
                ,'D|A':'010101'}
    return processed_comp + comp_dict[comp]

def destination_processing(dest):
    dest_list = ['A', 'D', 'M']
    processed_dest = ""
    for mem in dest_list:
        processed_dest += str(int(mem in dest))
    return processed_dest

def jump_processing(jump):
    jump_labels = ['L', 'E', 'G']
    processed_jump = ''
    for label in jump_labels:
        if 'N' in jump: 
            processed_jump += str(int(label not in jump))
        else:
            processed_jump += str(int(label in jump))
    if jump == 'JMP':
        processed_jump = '111'
    return processed_jump

def c_instructions_processing(line):
    line = seperate_instruction_fields(line)
    result = '111' + computation_processing(line[0]) + destination_processing(line[1]) + jump_processing(line[2]) + '\n'
    return result

in_file = open(sys.argv[1], "r")
out_file = open(sys.argv[1].replace(".asm", "Assembler.hack"), "w")

code_data = in_file.read().split("\n")

predefined_symbols = {'SP':0
                    ,'LCL':1
                    ,'ARG':2
                    ,'THIS':3
                    ,'THAT':4
                    ,'SCREEN':16384
                    ,'KBD':24576}
for memory_area in range(0,16):
    predefined_symbols['R' + str(memory_area)] = memory_area

label_symbols = {}

variable_symbols = {}

memory_counter = 16

line_no = 0

#Line counting for label symbols, to replace labels later on
for line in code_data:
    line = line.strip()
    line = line.split(" ")[0]
    if len(line) > 0:
        if line[0] == '(':
            label_symbols[line.strip('()')] = line_no
        elif line[0] != '/':
            line_no += 1

#Variable symbols processing, to assign new variables to memory segments (from RAM[16])
for line in code_data:
    line = line.strip()
    line = line.split(" ")[0]
    if len(line) > 0:
        if line[0] == '@':
            check_val = line[1:len(line)]
            if not check_val.isnumeric():
                if check_val not in label_symbols and check_val not in variable_symbols and check_val not in predefined_symbols:
                    variable_symbols[check_val] = memory_counter
                    memory_counter += 1

#Translate instructions to machine code
for line in code_data:
    line = line.strip()
    line = line.split(" ")[0]
    if len(line) >= 2:
        if line[0:2] != "//" and line[0] != '(':
            if line[0] == "@":
                out_file.write(a_instructions_processing(line))
            else:
                out_file.write(c_instructions_processing(line))
    else:
        if len(line) != 0:
            out_file.write(c_instructions_processing(line))

in_file.close()
out_file.close()