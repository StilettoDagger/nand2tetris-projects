class Code:
    def __init__(self):
        pass
    
    def translate_a(self, inst: int):
        binary = bin(inst).replace("0b", "")
        if len(binary) < 16:
            result = "0" * (16 - len(binary)) + binary
            return result
    
    def translate_comp(self, c):
        a = 0
        if "M" in c:
            c = c.replace("M", "A")
            a = 1
        if c == "0":
            return f"{a}101010"
        elif c == "1":
            return f"{a}111111"
        elif c == "-1":
            return f"{a}111010"
        elif c == "D":
            return f"{a}001100"
        elif c == "A":
            return f"{a}110000"
        elif c == "!D":
            return f"{a}001101"
        elif c == "!A":
            return f"{a}110001"
        elif c == "-D":
            return f"{a}001111"
        elif c == "-A":
            return f"{a}110011"
        elif c == "D+1":
            return f"{a}011111"
        elif c == "A+1":
            return f"{a}110111"
        elif c == "D-1":
            return f"{a}001110"
        elif c == "A-1":
            return f"{a}110010"
        elif c == "D+A":
            return f"{a}000010"
        elif c == "D-A":
            return f"{a}010011"
        elif c == "A-D":
            return f"{a}000111"
        elif c == "D&A":
            return f"{a}000000"
        elif c == "D|A":
            return f"{a}010101"
        
    def translate_dest(self, d):
        m = 0
        d_reg = 0
        a_reg = 0
        if d == "0":
            return "000"
        if "M" in d:
            m = 1
        if "D" in d:
            d_reg = 1
        if "A" in d:
            a_reg = 1
        return f"{a_reg}{d_reg}{m}"
            
        
    def translate_jump(self, j):
        g = 0
        e = 0
        l = 0
        if j == "0":
            return "000"
        if j == "JMP":
            return "111"
        if "G" in j:
            g = 1
        if "L" in j:
            l = 1
        if "E" in j and "N" not in j:
            e = 1
        if "N" in j:
            g = 1
            l = 1
            e = 0
        return f"{l}{e}{g}"
    
    def translate_c(self, command):
        comp = self.translate_comp(command[0])
        dest = self.translate_dest(command[1])
        jump = self.translate_jump(command[2])
        return f"111{comp}{dest}{jump}"
        
         
