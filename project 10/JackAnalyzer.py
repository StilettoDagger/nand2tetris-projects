import os
import sys
from compilation_engine import CompilationEngine


def main():
    path = sys.argv[1]

    if os.path.isdir(path):
        files_list = [path + "/" + f for f in os.listdir(path) if f.endswith(".jack")]
        for file in files_list:
            tokenizer = CompilationEngine(file)
    else:
        tokenizer = CompilationEngine(path)

    print("Successfully compiled xml file(s).")

if __name__ == "__main__":
    main()

