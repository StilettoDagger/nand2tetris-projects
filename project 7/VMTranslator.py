import sys
import os
from vm_parser import Parser
from vm_code_writer import CodeWriter

def main():
    vm_file = sys.argv[1]
    try:
        vm_parser = Parser(vm_file)
    except FileNotFoundError:
        print("Invalid filename/path")
        return None

    lines = vm_parser.parse()
    vm_parser.close()

    output_file = vm_file.replace(".vm", ".asm")

    code_writer = CodeWriter(lines, output_file)
    code_writer.translate()
    code_writer.close()

    print(f"Successfully compiled {os.path.basename(output_file)}")

if __name__ == "__main__":
    main()
