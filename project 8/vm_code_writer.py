import os

C_ARITHMETICS = ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not")
C_MEMORY = {"local": "LCL",
			"argument": "ARG",
			 "this": "THIS",
			  "that": "THAT"}
C_POINTERS = {"0": "THIS",
			  "1": "THAT"
}
C_BRANCHING = ("goto", "if-goto", "label")

class CodeWriter:
	"""
		This class is responsible for translating a given parsed code from VM code language into Hack assembly language.
		
		It also generates an .asm assembly output file with the translated code.

		Constructor Parameters:
		- parsed_lines(list): The list of the parsed commands that are to be translated	.
		- output_file(str): The name and path of the output file.
	"""
	def __init__(self, parsed_lines, output_filename, is_sys) -> None:
		self.lines = parsed_lines
		self.count = 0
		self.call_count = 0
		self.name = os.path.basename(output_filename).replace(".asm", "")
		self.file = open(output_filename, "w")
		self.is_sys = is_sys
		self.func_name = ""
		if self.is_sys:
			self.write_init()

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
			elif line[0] in ("push", "pop"):
				result = self.translate_memory(line)
				self.file.write(result)
			elif line[0] in C_BRANCHING:
				result = self.translate_branching(line)
				self.file.write(result)
			elif line[0] == "function":
				result = self.translate_function(line[1], line[2])
				self.func_name = line[1]
				self.file.write(result)
			elif line == "return":
				result = self.translate_return()
				self.file.write(result)
			elif line[0] == "call":
				result = self.translate_call(line[1], line[2])
				self.call_count += 1
				self.file.write(result)
		self.call_count = 0
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
			if self.is_sys:
				name = self.func_name.split(".")[0]
			if command[0] == "push":
				result = f"@{name}.{i}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"
			else:
				result = f"@SP\nM=M-1\nA=M\nD=M\n@{name}.{i}\nM=D\n"
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
	
	def translate_branching(self, command):
		"""
		Translate a branching command based on the given command type and target.

		-param command: A list containing the command type and target
		-return: The translated assembly code for the given command
		"""
		if command[0] == "label":
			if self.is_sys:
				return f"({self.func_name}.{command[1]})\n"
			else:
				return f"({command[1]})\n"
		elif command[0] == "goto":
			if self.is_sys:
				return f"@{self.func_name}.{command[1]}\n0;JMP\n"
			else:
				return f"@{command[1]}\n0;JMP\n"
		elif command[0] == "if-goto":
			if self.is_sys:
				return f"@SP\nM=M-1\nA=M\nD=M\n@{self.func_name}.{command[1]}\nD;JNE\n"
			else:
				return f"@SP\nM=M-1\nA=M\nD=M\n@{command[1]}\nD;JNE\n"
		
	def translate_function(self, f_name, n_vars):
		result = f"({f_name})\n"
		for i in range(int(n_vars)):
			result += self.translate_memory(("push", "constant", "0"))
			result += self.translate_memory(("pop", "local", str(i)))
			result += self.translate_memory(("push", "local", str(i)))
		return result

	def translate_return(self):
		return "@LCL\nD=M\n@R13\nM=D\n@R5\nD=D-A\nA=D\nD=M\n@R14\nM=D\n@SP\nA=M-1\nD=M\n@ARG\nA=M\nM=D\n@ARG\nD=M\n@SP\nM=D\nM=M+1\n@R13\nM=M-1\nA=M\nD=M\n@THAT\nM=D\n@R13\nM=M-1\nA=M\nD=M\n@THIS\nM=D\n@R13\nM=M-1\nA=M\nD=M\n@ARG\nM=D\n@R13\nM=M-1\nA=M\nD=M\n@LCL\nM=D\n@R14\nA=M\n0;JMP\n"

	def translate_call(self, f_name, n_args):
		return f"@{f_name}$ret.{self.call_count}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n@{n_args}\nD=A\n@5\nD=D+A\n@SP\nD=M-D\n@ARG\nM=D\n@SP\nD=M\n@LCL\nM=D\n@{f_name}\n0;JMP\n({f_name}$ret.{self.call_count})\n"

	def write_init(self):
		bootstrap_code = "@256\nD=A\n@SP\nM=D\n" + self.translate_call("Sys.init", "0")
		self.file.write(bootstrap_code)

	def close(self):
		self.file.close()