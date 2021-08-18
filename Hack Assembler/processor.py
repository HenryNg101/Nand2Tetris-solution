#This module is used to process different types of instructions, computations and jumps

import preprocess

class InstructionProcessor:
    def __init__(self, code_data, out_file):
        self.predefined_symbols, self.label_symbols, self.variable_symbols = preprocess.define(code_data)
        self.translate(code_data, out_file, self.label_symbols, self.variable_symbols, self.predefined_symbols)

    def translate(self, code_data, out_file, label_symbols, variable_symbols, predefined_symbols):
        for line in code_data:
            line = line.strip()
            line = line.split(" ")[0]
            if len(line) >= 2:
                if line[0:2] != "//" and line[0] != '(':
                    if line[0] == "@":
                        out_file.write(self.a_instructions_processing(line, label_symbols, variable_symbols, predefined_symbols))
                    else:
                        out_file.write(self.c_instructions_processing(line))
            else:
                if len(line) != 0:
                    out_file.write(self.c_instructions_processing(line))
        out_file.close()

    def a_instructions_processing(self, line, label_symbols, variable_symbols, predefined_symbols):
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

    def c_instructions_processing(self, line):
        line = self.seperate_instruction_fields(line)
        result = '111' + self.computation_processing(line[0]) + self.destination_processing(line[1]) + self.jump_processing(line[2]) + '\n'
        return result

    def seperate_instruction_fields(self, line):
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

    def computation_processing(self, comp):
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

    def destination_processing(self, dest):
        dest_list = ['A', 'D', 'M']
        processed_dest = ""
        for mem in dest_list:
            processed_dest += str(int(mem in dest))
        return processed_dest

    def jump_processing(self, jump):
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