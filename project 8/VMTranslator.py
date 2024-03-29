import sys
import os
from vm_parser import Parser
from vm_code_writer import CodeWriter

def main():
	path = sys.argv[1]
	if (os.path.isfile(path)):
		try:
			vm_parser = Parser(path)
		except FileNotFoundError:
			print("Invalid filename/path")
		output_file = path.replace(".vm", ".asm")
		lines = vm_parser.parse()
		# print(lines)
		vm_parser.close()
		write_code(output_file, lines, is_sys= False)
	else:
		vm_list = [f for f in os.listdir(path) if f.endswith(".vm") and f != "Sys.vm"]
		vm_parser = Parser(path + "/Sys.vm")
		lines = vm_parser.parse()
		vm_parser.close()
		for f in vm_list:
			vm_parser = Parser(path + "/" + f)
			lines += vm_parser.parse()
			vm_parser.close()
		# print(lines)
		output_file = os.path.basename(os.path.normpath(path)) + ".asm"
		write_code(path + "/" + output_file, lines, is_sys= True)
		   

def write_code(filename, parsed_lines, is_sys):

	code_writer = CodeWriter(parsed_lines, filename, is_sys)
	code_writer.translate()
	code_writer.close()

	print(f"Successfully compiled {os.path.basename(filename)}")

if __name__ == "__main__":
	main()
