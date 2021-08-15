import CompilationEngine
import sys
import pathlib

def compile(path):
    in_file = open(path, 'r')
    out_file = open(path.replace(".jack", "_test.vm"), 'w')
    code_data = in_file.read()
    obj = CompilationEngine.Parser(code_data)
    out_file.write(obj.code)

in_name = sys.argv[1]

if in_name[-5:len(in_name)] == '.jack':
    compile(in_name)
else:
    directory = pathlib.Path(in_name).glob('*.jack')
    for jack_file in directory:
        compile(in_name + "/" + jack_file.name)