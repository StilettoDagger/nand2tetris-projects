class Parser:
    def __init__(self):
        pass
        
    def parse_a(self, command):
        address = command.split('@')[1]
        if not address.isnumeric():
            return address
        else:
            return int(address)
    
    def comp(self, command):
        if '=' in command:
            if ';' in command:
                return command.split('=')[1].split(';')[0]
            else:
                return command.split('=')[1]
        elif "D" in command:
            return "D"
        else:
            return "0"
        
    def dest(self, command):
        if '=' in command:
            return command.split('=')[0]
        else:
            return "0"
    
    def jump(self, command):
        if ';' in command:
            return command.split(';')[1]
        else:
            return "0"
        
    def parse_c(self, command):
        c = self.comp(command)
        d = self.dest(command)
        j = self.jump(command)
        return (c, d, j)
