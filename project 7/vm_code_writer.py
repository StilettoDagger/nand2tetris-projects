import os

C_ARITHMETICS = ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not")
C_MEMORY = {"local": "LCL",
			"argument": "ARG",
			 "this": "THIS",
			  "that": "THAT"}
C_POINTERS = {"0": "THIS",
			  "1": "THAT"
}

class CodeWriter:
	"""
		This class is responsible for translating a given parsed code from VM code language into Hack assembly language.
		
		It also generates an .asm assembly output file with the translated code.

		Constructor Parameters:
		- parsed_lines(list): The list of the parsed commands that are to be translated	.
		- output_file(str): The name and path of the output file.
	"""
	def __init__(self, parsed_lines, output_filename) -> None:
		self.lines = parsed_lines
		self.count = 0
		self.name = os.path.basename(output_filename).replace(".asm", "")
		self.file = open(output_filename, "w")

	def translate(self):
		"""
		Translate function that processes each line and writes the translation to a file.
		
		The function uses the functions translate_arithmetic() and translate_memory() to handle arithmetic
		and memory VM code commands respectively.
		"""
		for line in self.lines:
			if line in C_ARITHMETICS:
				result = self.translate_arithmetic(line)
				self.file.write(result)
			else:
				result = self.translate_memory(line)
				self.file.write(result)
	

	def translate_arithmetic(self, command):
		"""
		Generate the machine code translation for VM code arithmetic operation commands.

		Parameters:
		- command (str): The command to be translated into machine code.

		Returns:
		- str: The machine code translation for the given command.
		"""

		arg1 = "@SP\nA=M\nA=A-1\nA=A-1\nD=M\n"
		arg2 = "@SP\nA=M\nA=A-1\n"
		self.count += 1

		if command == "add":
			result = arg1 + "A=A+1\nD=D+M\nA=A-1\nM=D\n@SP\nM=M-1\n"
		elif command == "sub":
			result = arg1 + "A=A+1\nD=D-M\nA=A-1\nM=D\n@SP\nM=M-1\n"
		elif command == "neg":
			result = arg2 + "M=-M\n"
		elif command == "eq":
			result = arg1 + f"A=A+1\nD=D-M\nA=A-1\nM=0\n@EQUALS.{self.count}\nD;JEQ\n@END.{self.count}\n0;JMP\n(EQUALS.{self.count})\n@SP\nA=M\nA=A-1\nA=A-1\nM=-1\n(END.{self.count})\n@SP\nM=M-1\n"
		elif command == "gt":
			result = arg1 + f"A=A+1\nD=D-M\nA=A-1\nM=0\n@GT.{self.count}\nD;JGT\n@END.{self.count}\n0;JMP\n(GT.{self.count})\n@SP\nA=M\nA=A-1\nA=A-1\nM=-1\n(END.{self.count})\n@SP\nM=M-1\n"
		elif command == "lt":
			result = arg1 + f"A=A+1\nD=D-M\nA=A-1\nM=0\n@LT.{self.count}\nD;JLT\n@END.{self.count}\n0;JMP\n(LT.{self.count})\n@SP\nA=M\nA=A-1\nA=A-1\nM=-1\n(END.{self.count})\n@SP\nM=M-1\n"
		elif command == "and":
			result = arg1 + "A=A+1\nD=D&M\nA=A-1\nM=D\n@SP\nM=M-1\n"
		elif command == "or":
			result = arg1 + "A=A+1\nD=D|M\nA=A-1\nM=D\n@SP\nM=M-1\n"
		elif command == "not":
			result = arg2 + "M=!M\n"
		else:
			return None
		
		return result
			
	def translate_memory(self, command):
		"""
		Generate the machine code translation for the given VM code command based on the specified memory segment.
		
		Parameters:
		- command: a list containing the command type, memory segment, and index
		
		Returns:
		- result: a string representing the translated machine code for the command
		"""

		i = command[2]
		if command[1] in C_MEMORY:
			if command[0] == "push":
				result = f"@{i}\nD=A\n@{C_MEMORY[command[1]]}\nD=D+M\nA=D\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			else:
				result = f"@{i}\nD=A\n@{C_MEMORY[command[1]]}\nD=D+M\n@R13\nM=D\n@SP\nM=M-1\nA=M\nD=M\n@R13\nA=M\nM=D\n"

		elif command[1] == "constant":
			result = f"@{i}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
		
		elif command[1] == "static":
			if command[0] == "push":
				result = f"@{self.name}.{i}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			else:
				result = f"@SP\nM=M-1\nA=M\nD=M\n@{self.name}.{i}\nM=D\n"
		elif command[1] == "temp":
			temp_index = 5 + int(i)
			if command[0] == "push":
				result = f"@{temp_index}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			else:
				result = f"@SP\nM=M-1\nA=M\nD=M\n@{temp_index}\nM=D\n"
		elif command[1] == "pointer":
			if command[0] == "push":
				result = f"@{C_POINTERS[i]}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			else:
				result = f"@SP\nM=M-1\nA=M\nD=M\n@{C_POINTERS[i]}\nM=D\n"

		return result
	
	def close(self):
		self.file.close()