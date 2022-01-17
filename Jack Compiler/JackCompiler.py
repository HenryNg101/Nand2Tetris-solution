import pathlib
import argparse
import importlib

class JackCompiler:
    def __init__(self, generate_true, path):
        self.out_type = {'.vm':importlib.import_module('CompilationEngine'), '.xml':importlib.import_module('JackParser')}
        self.generate_true = generate_true
        self.compile(path)

    def compile(self, path):
        for file_extension in self.out_type:
            if file_extension == '.xml' and not self.generate_true:
                continue
            in_file = open(path, 'r')
            out_file = open(path.replace(".jack", file_extension), 'w')
            code_data = in_file.read()
            obj = self.out_type[file_extension].Parser(code_data)
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
    JackCompiler(generate_true, in_name)
else:
    directory = pathlib.Path(in_name).glob('*.jack')
    for jack_file in directory:
        JackCompiler(generate_true, in_name + "/" + jack_file.name)