import parser
import tokenizer
import sys
import xml.etree.ElementTree as ET

in_name = sys.argv[1] 
in_file = open(in_name, 'r')
out_file = open(in_name.replace(".jack", "_test.xml"), 'w')
code_data = in_file.read()

obj = tokenizer.Tokenizer(code_data)

#out_file.write(obj.tokens)
top = ET.Element('class')
arr = obj.tokens
result = ET.tostring(top, encoding='unicode')
print(arr)