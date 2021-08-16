import CompilationEngine
import JackParser
import pathlib
import argparse

def generate_parse_tree(path):
    in_file = open(path, 'r')
    out_file = open(path.replace(".jack", ".xml"), 'w')
    code_data = in_file.read()
    obj = JackParser.Parser(code_data)
    out_file.write(obj.xml)
    in_file.close()
    out_file.close()

def compile(path):
    in_file = open(path, 'r')
    out_file = open(path.replace(".jack", ".vm"), 'w')
    code_data = in_file.read()
    obj = CompilationEngine.Parser(code_data)
    out_file.write(obj.code)
    in_file.close()
    out_file.close()

arg_parser = argparse.ArgumentParser(description="The Jack Compiler, used to compile Jack to VM code")
arg_parser.add_argument('-p', '--parse-tree', action='store_true', help='To generate parse tree as an XML file', required=False)
arg_parser.add_argument('filename')     #Required .jack file
arg = arg_parser.parse_args()

in_name = arg.filename
generate_true = arg.parse_tree

if in_name[-5:len(in_name)] == '.jack':
    compile(in_name)
    if generate_true:
        generate_parse_tree(in_name)
else:
    directory = pathlib.Path(in_name).glob('*.jack')
    for jack_file in directory:
        compile(in_name + "/" + jack_file.name)
        if generate_true:
            generate_parse_tree(in_name + "/" + jack_file.name)