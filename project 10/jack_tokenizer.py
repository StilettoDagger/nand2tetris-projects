import re
import html
import os

KEYWORDS = ("class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return")
SYMBOLS = ("{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~")

pattern = r"("
for k in KEYWORDS:
    pattern += r"\b" + k + r"\b|"

pattern = pattern[:-1]

for s in SYMBOLS:
    pattern += f"|\\{s}"

pattern += r'|".*?"|\w+|\d+)'

# print(pattern)

class JackTokenizer:
    def __init__(self, file_name) -> None:
        self.file = open(file_name)
        self.code = self.file.read()
        self.code = re.sub(r"//.*", '', self.code)
        self.code = re.sub(r"/\*.*?\*/", '', self.code, flags=re.DOTALL)
        self.token_count = 0
        self.tokens = re.findall(pattern, self.code)
        # print(self.tokens)
        self.current_token = ""
        self.current_token_type = ""
        self.next_token = ""
        self.output_string = ""
        self.output_string += "<tokens>\n"
        while self.has_more_tokens():
            self.advance()
        self.output_string += "</tokens>\n"
        # self.output_dir = "./xml/" + os.path.dirname(file_name).replace("./", "")
        # if not os.path.exists(self.output_dir):
        #     os.mkdir(self.output_dir)
        # self.token_output_file = self.output_dir + "/" + os.path.basename(file_name).replace(".jack", "T.xml")
        self.token_output_file = file_name.replace(".jack", "T.xml")
        with open(self.token_output_file, "w") as t_file:
            t_file.write(self.output_string)

    def has_more_tokens(self):
        if self.token_count < len(self.tokens):
            return True
        else:
            return False
        
    def advance(self):
        if not self.has_more_tokens():
            return

        self.current_token = self.tokens[self.token_count]
        self.next_token = self.tokens[self.token_count + 1] if self.token_count + 1 < len(self.tokens) else None

        if self.current_token in KEYWORDS:
            self.current_token_type = "keyword"
        elif self.current_token in SYMBOLS:
            self.current_token_type = "symbol"
        elif '"' in self.current_token:
            self.current_token = self.current_token.strip('"')
            self.current_token_type = "stringConstant"
        elif self.current_token.isdigit():
            self.current_token_type = "integerConstant"
        else:
            self.current_token_type = "identifier"

        self.output_string += f"<{self.current_token_type}>{html.escape(self.current_token)}</{self.current_token_type}>\n"
        self.token_count += 1
    
    def token_type(self):
        return self.current_token_type
    
    def key_word(self):
        if self.token_type() == "keyword":
            return self.current_token
        else:
            return None
        
    def symbol(self):
        if self.token_type() == "symbol":
            return self.current_token
        else:
            return None
    
    def identifier(self):
        if self.token_type() == "identifier":
            return self.current_token
        else:
            return None
        
    def int_val(self):
        if self.token_type() == "integerConstant":
            return self.current_token_type
        else:
            return None
        
    def string_val(self):
        if self.token_type() == "stringConstant":
            return self.current_token_type
        else:
            return None