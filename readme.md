# Tokenizer

This is a simple tokenizer in Python 3. It is in two layers:
- A line tokenizer
- A token buffer that handles one or more files

The tokenizer automatically provides 'wHITE_SPACE' and 'UNKNOWN'. White space is collected together and unknown tokens are individual characters.

Token_Buffer.config offers access to tokenizing flags:
- skip_white_space: peek will not return whitespace.
- skip_EOF: The end of file is marked internally for the sake of tracking position. The setting skip_EOF can be set to False to include these tokens in the token stream. This is handy for files that have ignored preamble.

Example program:
```python
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
    "DIVIDE": r"\\",
    "EXPONENT": r"\^",
    "TETRATION": r"\^\^",
    "IDENTIFIER": r"[\w_]+",
    "OPEN_PAREN": r"\(",
    "CLOSE_PAREN": r"\)",
}

buffer = tb.TokenBuffer()
buffer.init_patterns(patterns)
buffer.load_files(sys.argv[1:])
buffer.config(skip_white_space = True)
buffer.tokenize()

while not buffer.out_of_tokens():
    peek = buffer.peek()
    file, line, column = buffer.get_position()
    print(f'{file} {line} {column} Token: type = {peek.type}, value = {peek.value}')
    buffer.consume()
```