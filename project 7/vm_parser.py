C_ARITHMETIC = ("add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not")

class Parser:
    """
        This class is responsible for opening the original VM source code, parsing its lines,
        and breaking it down into its important elements while ignoring all white space and comments.

        Constructor Parameters:
        -filename (str): The name of the input file that needs to be opened and parsed.
    """
    def __init__(self, filename) -> None:
        self.file = open(filename, "r")
        self.lines = self.file.readlines()
        self.parsed_lines = []

    def parse(self):
        """
        Parse the lines of the input file and return a list of parsed lines.
        """
        for line in self.lines:
            if "/" not in line and line[0] != "\n":
                if line.strip() in C_ARITHMETIC:
                    self.parsed_lines.append(line.strip())
                else:
                    # Split the line if it's a memory command into three parts (push/pop, memory segment, and index) and output the parsed line as a tuple of size 3
                    mem_line = tuple(line.strip().split(" "))
                    self.parsed_lines.append(mem_line)
        return self.parsed_lines
    
    def close(self):
        self.file.close()
                    
    

