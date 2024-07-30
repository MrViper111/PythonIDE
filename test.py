import ast
import tokenize
import io
from itertools import groupby
from operator import itemgetter


class Token:
    def __init__(self, label, color):
        self.label = label
        self.color = color

    def __repr__(self):
        return f"Token({self.label!r}, {self.color!r})"


# ok this is HORRIBLE
# wtf have I done
def get_color(token, color_map, context=None):
    keywords = {"def", "if", "True"}
    if token in keywords:
        return color_map['keywords']
    elif context == "function":
        return color_map['functions']
    elif context == "string":
        return color_map['strings']
    elif token.isidentifier():
        return color_map['variables']
    else:
        return 'white'


def merge(tokens):
    label = "".join([token.label for token in tokens])
    color = tokens[0].color
    return Token(label, color)


def merge_adjacent_tokens(lines):
    merged_lines = []
    for line in lines:
        merged_line = []
        for color, group in groupby(line, key=lambda t: t.color):
            merged_line.append(merge(list(group)))
        merged_lines.append(merged_line)
    return merged_lines


class CodeTokenizer(ast.NodeVisitor):
    def __init__(self, code, color_map):
        self.color_map = color_map
        self.token_data = self.tokenize_code(code)
        self.ast_tree = ast.parse(code)
        self.lines = self.build_lines()
        self.update_token_colors()

    def tokenize_code(self, code):
        return list(tokenize.generate_tokens(io.StringIO(code).readline))

    def build_lines(self):
        lines = []
        current_line = []
        for toknum, tokval, start, _, _ in self.token_data:
            if tokval == '\n':
                if current_line:
                    lines.append(current_line)
                current_line = []
            else:
                color = self.get_token_color(tokval, start)
                current_line.append(Token(tokval, color))
        if current_line:
            lines.append(current_line)
        return lines

    def get_token_color(self, tokval, start):
        for node in ast.walk(self.ast_tree):
            if hasattr(node, 'lineno') and node.lineno == start[0]:
                if isinstance(node, ast.FunctionDef) and node.name == tokval:
                    return self.color_map['functions']
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == tokval:
                    return self.color_map['functions']
                if isinstance(node, ast.Name) and node.id == tokval:
                    return self.color_map['variables']
                if isinstance(node, (ast.Str, ast.Constant)) and isinstance(node.s, str) and node.s == tokval:
                    return self.color_map['strings']
        return get_color(tokval, self.color_map)

    def update_token_colors(self):
        for node in ast.walk(self.ast_tree):
            if isinstance(node, ast.FunctionDef):
                self.replace_token_color(node.name, self.color_map['functions'])
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                self.replace_token_color(node.func.id, self.color_map['functions'])
            elif isinstance(node, ast.Name):
                self.replace_token_color(node.id, self.color_map['variables'])
            elif isinstance(node, (ast.Str, ast.Constant)) and isinstance(node.s, str):
                self.replace_token_color(f'"{node.s}"', self.color_map['strings'])

    def replace_token_color(self, target, color):
        for line in self.lines:
            for token in line:
                if token.label == target:
                    token.color = color


def parse_code_to_tokens(code, color_map):
    tokenizer = CodeTokenizer(code, color_map)
    return merge_adjacent_tokens(tokenizer.lines)


# Example usage
code = """def foo():
    print("Hello world!")

should_print = True
if should_print:
    foo()"""

color_map = {
    "keywords": "orange",
    "variables": "blue",
    "functions": "yellow",
    "strings": "green"
}

token_content = parse_code_to_tokens(code, color_map)
for line in token_content:
    print(line)
