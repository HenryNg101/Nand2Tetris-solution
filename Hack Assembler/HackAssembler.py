import sys
import pathlib
import argparse
import processor

def translate(path):
    in_file = open(path, 'r')
    out_file = open(path.replace(".asm", ".hack"), 'w')
    code_data = in_file.read().split('\n')
    processor.InstructionProcessor(code_data, out_file)
    in_file.close()

arg_parser = argparse.ArgumentParser(description="The Hack Assembler, used to translate Hack Assembly into binary code")
arg_parser.add_argument('filename')     #Required .asm file (Or folder)
arg = arg_parser.parse_args()

in_name = arg.filename

if in_name[-4:len(in_name)] == '.asm':
    translate(in_name)
else:
    directory = pathlib.Path(in_name).glob("*.asm")
    for asm_file in directory:
        translate(in_name + '/' + asm_file.name)