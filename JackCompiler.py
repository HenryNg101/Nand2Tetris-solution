import JackParser
import sys
import xml.etree.ElementTree as ET

in_name = sys.argv[1] 
in_file = open(in_name, 'r')
out_file = open(in_name.replace(".jack", "_test.xml"), 'w')
code_data = in_file.read()

obj = JackParser.Parser(code_data)

out_file.write(obj.xml)