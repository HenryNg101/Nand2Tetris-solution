#This module is used to all types of symbols (predefined, label and variable)

#Define all types of symbols and return them
def define(code_data):
    predefined_symbols = {'SP':0
                        ,'LCL':1
                        ,'ARG':2
                        ,'THIS':3
                        ,'THAT':4
                        ,'SCREEN':16384
                        ,'KBD':24576}
    for memory_area in range(0,16):
        predefined_symbols['R' + str(memory_area)] = memory_area
    label_symbols = label_processing(code_data)
    variable_symbols = variable_processing(code_data, label_symbols, predefined_symbols)
    return predefined_symbols, label_symbols, variable_symbols

#Line counting for label symbols, to replace labels with line number later on
def label_processing(code_data):
    label_symbols = {}
    line_no = 0
    for line in code_data:
        line = line.strip()
        line = line.split(" ")[0]
        if len(line) > 0:
            if line[0] == '(':
                label_symbols[line.strip('()')] = line_no
            elif line[0] != '/':
                line_no += 1
    return label_symbols

#Variable symbols processing, to assign new variables to memory segments (from RAM[16])
def variable_processing(code_data, label_symbols, predefined_symbols):
    variable_symbols = {}
    memory_counter = 16
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
    return variable_symbols