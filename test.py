import TokenBuffer as tb
import sys

if len(sys.argv) < 2:
    print('Please provide one or more files to tokenize')
    exit(1)

patterns = {
    "INTEGER": r"\d+",
    "ASSIGNMENT": r"=",
    "PLUS": r"\+",
    "MINUS": r"\-",
    "MULTIPLY": r"\*",
    "DIVIDE": r"/",
    "TETRATION": r"\^\^",
    "EXPONENT": r"\^",
    "IDENTIFIER": r"[\w_]+",
    "OPEN_PAREN": r"\(",
    "CLOSE_PAREN": r"\)",
}

buffer = tb.TokenBuffer()
buffer.init_patterns(patterns)
buffer.load_files(sys.argv[1:])
buffer.config(skip_white_space = True, skip_EOF = False)
buffer.tokenize()

while not buffer.out_of_tokens():
    peek = buffer.peek()
    if peek:
        file, line, column = buffer.get_position()
        print(f"{file} {line} {column} Token: type = {peek.type}, value = '{'' if not peek.value else peek.value}'")
        buffer.consume()
    