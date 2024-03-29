from jack_tokenizer import JackTokenizer
import os

STATEMENTS = ("let", "if", "while", "do", "return")
OPERATORS = ("+", "-", "*", "/", "&", "<", ">", "=", "|")
class CompilationEngine(JackTokenizer):
    def __init__(self, input_file):
        super().__init__(input_file)
        self.output_string = ""
        self.token_count = 0
        self.compile_class()
        # print(self.output_string)
        # self.output_dir = "./xml/" + os.path.dirname(input_file).replace("./", "")
        # if not os.path.exists(self.output_dir):
        #     os.mkdir(self.output_dir)
        # self.output_file = self.output_dir + "/" + os.path.basename(input_file).replace(".jack", ".xml")
        self.output_file = input_file.replace(".jack", ".xml")
        with open(self.output_file, "w") as xml_file:
            xml_file.write(self.output_string)
    
    def compile_class(self):
        self.output_string += "<class>\n"
        self.advance()  # class keyword
        self.advance()  # class name
        self.advance()  # '{' symbol
        while self.next_token in ("static", "field"):
            self.compile_class_var_dec()
        while self.next_token in ("constructor", "function", "method"):
            self.compile_subroutine_dec()
        self.advance()  # '}' symbol
        self.output_string += "</class>\n"
        return
    
    def compile_class_var_dec(self):
        self.output_string += "<classVarDec>\n"
        self.advance()  # static or field
        self.advance()  # type
        self.advance()  # varName
        while self.next_token == ",":
            self.advance()  # ',' symbol
            self.advance()  # varName
        self.advance()  # ';' symbol
        self.output_string += "</classVarDec>\n"
        return
    
    def compile_subroutine_dec(self):
        self.output_string += "<subroutineDec>\n"
        self.advance()  # constructor, function, or method
        self.advance()  # void or type
        self.advance()  # subroutineName
        self.advance()  # '(' symbol
        self.compile_parameter_list()
        self.advance()  # ')' symbol
        self.compile_subroutine_body()
        self.output_string += "</subroutineDec>\n"
        return

    def compile_parameter_list(self):
        self.output_string += "<parameterList>\n"
        if self.next_token != ")":
            self.advance()  # type
            self.advance()  # varName
            while self.next_token == ",":
                self.advance()  # ',' symbol
                self.advance()  # type
                self.advance()  # varName
        self.output_string += "</parameterList>\n"
        return
    
    def compile_subroutine_body(self):
        self.output_string += "<subroutineBody>\n"
        self.advance()  # '{' symbol
        while self.next_token == "var":
            self.compile_var_dec()
        self.compile_statements()
        self.advance()  # '}' symbol
        self.output_string += "</subroutineBody>\n"
        return
    
    def compile_var_dec(self):
        self.output_string += "<varDec>\n"
        self.advance()  # var keyword
        self.advance()  # type
        self.advance()  # varName
        while self.next_token == ",":
            self.advance()  # ',' symbol
            self.advance()  # varName
        self.advance()  # ';' symbol
        self.output_string += "</varDec>\n"
        return
    
    def compile_statements(self):
        self.output_string += "<statements>\n"
        while self.next_token in STATEMENTS:
            if self.next_token == "let":
                self.compile_let()
            elif self.next_token == "if":
                self.compile_if()
            elif self.next_token == "while":
                self.compile_while()
            elif self.next_token == "do":
                self.compile_do()
            elif self.next_token == "return":
                self.compile_return()
        self.output_string += "</statements>\n"
        return
    
    def compile_let(self):
        self.output_string += "<letStatement>\n"
        self.advance()  # let keyword
        self.advance()  # varName
        if self.next_token == "[":
            self.advance()  # '[' symbol
            self.compile_expression()
            self.advance()  # ']' symbol
        self.advance()  # '=' symbol
        self.compile_expression()
        self.advance()  # ';' symbol
        self.output_string += "</letStatement>\n"
        return
    
    def compile_if(self, is_else=False):
        self.output_string += "<ifStatement>\n"
        self.advance()  # if keyword
        self.advance()  # '(' symbol
        self.compile_expression()
        self.advance()  # ')' symbol
        self.advance()  # '{' symbol
        self.compile_statements()
        self.advance()  # '}' symbol
        if self.next_token == "else":
            self.compile_else()
        self.output_string += "</ifStatement>\n"
        return

    def compile_else(self):
        self.advance()  # else keyword
        self.advance()  # '{' symbol
        self.compile_statements()
        self.advance()  # '}' symbol
        return

    def compile_while(self):
        self.output_string += "<whileStatement>\n"
        self.advance()  # while keyword
        self.advance()  # '(' symbol
        self.compile_expression()
        self.advance()  # ')' symbol
        self.advance()  # '{' symbol
        self.compile_statements()
        self.advance()  # '}' symbol
        self.output_string += "</whileStatement>\n"
        return
    
    def compile_do(self):
        self.output_string += "<doStatement>\n"
        self.advance()  # do keyword
        self.compile_subroutine_call()
        self.advance()  # ';' symbol
        self.output_string += "</doStatement>\n"
        return
    
    def compile_return(self):
        self.output_string += "<returnStatement>\n"
        self.advance()  # return keyword
        if self.next_token != ";":
            self.compile_expression()
        self.advance()  # ';' symbol
        self.output_string += "</returnStatement>\n"
        return
    
    def compile_expression(self):
        self.output_string += "<expression>\n"
        self.compile_term()
        while self.next_token in OPERATORS:
            self.advance()  # op symbol
            self.compile_term()
        self.output_string += "</expression>\n"
        return
    
    def compile_term(self):
        self.output_string += "<term>\n"
        if self.next_token in ("-", "~"):
            self.advance()  # unaryOp symbol
            self.compile_term()
        elif self.next_token == "(":
            self.advance()  # '(' symbol
            self.compile_expression()
            self.advance()  # ')' symbol
        else:
            self.advance()  # varName or subroutineName or integerConstant or stringConstant or keywordConstant
            if self.next_token == "[":
                self.advance()  # '[' symbol
                self.compile_expression()
                self.advance()  # ']' symbol
            elif self.next_token in ("(", "."):
                self.advance()
                self.compile_subroutine_call()
        self.output_string += "</term>\n"
        return
    
    def compile_subroutine_call(self):
        if self.current_token != "(":
            self.advance()  # subroutineName or className or varName
            if self.next_token == ".":
                self.advance()  # '.' symbol
                self.advance()  # subroutineName 
            self.advance()
        self.compile_expression_list()
        self.advance()  # ')' symbol
        return
    
    def compile_expression_list(self):
        self.output_string += "<expressionList>\n"
        if self.next_token != ")":
            self.compile_expression()
            while self.next_token == ",":
                self.advance()  # ',' symbol
                self.compile_expression()
        self.output_string += "</expressionList>\n"
        return


