import sys
from hack_parser import Parser
from hack_coder import Code
from hack_symbols import SymbolTable

def first_pass(lines):
    address = 0
    for line in lines:
        if line[0] == '(':
            new_symbol = line.replace("(", "").replace(")", "")
            symbols.add_symbol(new_symbol, address)
        else:
            address += 1



file_name = sys.argv[1]

with open(file_name, "r") as f:
    lines = f.readlines()
    # Removes comments and empty lines form the file
    stripped_lines = [line.strip() for line in lines if "/" not in line and line != "" and line[0] != "\n"]

# Store the pre defined symbols in a python dictionary
symbols = SymbolTable()    
parser = Parser()
code = Code()

# Performs a first pass on the program code for storing the addresses of labels in the symbols table
first_pass(stripped_lines)

# print(symbols.table)
file_output = file_name.split("/")[2].replace("asm", "hack")

var_addr = 16

# Remove all the labels from the program code so that they are not parsed.
program_code = [line for line in stripped_lines if "(" not in line]

with open(file_output, "w") as f:
    for line in program_code:
        if line[0] == '@':
            a_inst = parser.parse_a(line)
            if type(a_inst) is not int:
                try:
                    address = symbols.table[a_inst]
                except KeyError:
                    # Adds a new variable and store it in the symbols table if the symbol was already found in the table.
                    address = var_addr
                    symbols.add_symbol(a_inst, address)
                    var_addr += 1
                a_inst = address
            # Translate the instruction into binary and write it in the output .hack file
            b_inst = code.translate_a(a_inst)
            f.write(f"{b_inst}\n")
        else:
            c_inst = parser.parse_c(line)
            b_inst = code.translate_c(c_inst)
            f.write(f"{b_inst}\n")

print(f"Successfully compiled {file_output}")