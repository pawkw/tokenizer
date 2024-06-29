from typing import List, Dict
from tokenizer import tokenize, Token
import re

class TokenBuffer:
    def __init__(self):
        self.column = 0
        self.line = 0
        self.files = []
        self.file_index = 0
        self.lines: List[List[Token]] = [[]]
        self.config = {
            'skip_white_space': False,
            'skip_EOF': True
        }

    def init_patterns(self, patterns: Dict):
        self.token_pattern_str = '|'.join([f"(?P<{key}>{value})" for key, value in patterns.items()])
        self.re_pattern = re.compile(self.token_pattern_str)
        if not self.re_pattern:
            raise ValueError("Unable to compile provided patterns.")
        
    def load_files(self, files: List[str]):
        self.files = files
        for file in self.files:
            with open(file, 'r') as source:
                lines = source.readlines()
                self.lines.append(lines)

    def config(self, **flags):
        for key, value in flags:
            self.config[key] = value

    def get_position(self):
        return self.files[self.file_index], self.line, self.column + 1

    def peek(self):
        while True:
            if (self.skip_white_space and self.expect_type('WHITE_SPACE') or \
            self.skip_EOF and self.expect_type('EOF')) and \
            not self.out_of_tokens():
                self.consume()
                continue
            break
        return None if self.out_of_tokens() else self.lines[self.line][self.column]

    def expect_value(self, expected_sting: str, lower: bool = False):
        return self.peek().value.tolower() == expected_sting if lower else self.peek().value == expected_sting

    def expect_type(self, expected_type: str):
        return self.peek().type == expected_type

    def consume(self):
        if self.expect_type('EOF'):
            self.file_index += 1
        self.column += 1
        if self.column > len(self.lines[self.line]):
            self.consume_line()

    def backtrack(self):
        pass

    def out_of_tokens(self):
        return self.line > len(self.lines)

    def consume_line(self):
        if self.out_of_tokens():
            raise IndexError("Attempt to consume line beyond end of program.")
        self.line += 1
        self.column = 0