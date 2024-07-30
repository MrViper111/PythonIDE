import ast
import tokenize
import io
import keyword

class Token:
    def __init__(self, label, color):
        self.label = label
        self.color = color

    def __repr__(self):
        return f"Token({self.label!r}, {self.color!r})"

def get_color(token, color_map, context=None):
    if keyword.iskeyword(token):
        return color_map['keywords']
    if context == "function":
        return color_map['functions']
    if context == "string":
        return color_map['strings']
    if token.isidentifier():
        return color_map['variables']
    return 'white'

class CodeTokenizer:
    def __init__(self, code, color_map):
        self.color_map = color_map
        self.tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
        try:
            self.ast_tree = ast.parse(code)
            self.token_colors = {}
            self.assign_colors()
        except SyntaxError:
            self.ast_tree = None
            self.token_colors = {}

    def assign_colors(self):
        if self.ast_tree:
            self.visit_node(self.ast_tree)

    def visit_node(self, node):
        if isinstance(node, ast.FunctionDef):
            self.set_color(node.name, 'functions')
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                self.set_color(node.func.id, 'functions')
        elif isinstance(node, ast.Name):
            self.set_color(node.id, 'variables')
        elif isinstance(node, ast.Constant) and isinstance(node.value, str):
            self.set_color(repr(node.value), 'strings')

        for child_node in ast.iter_child_nodes(node):
            self.visit_node(child_node)

    def set_color(self, label, context):
        self.token_colors[label] = get_color(label, self.color_map, context)

    def get_colored_tokens(self):
        colored_tokens = []
        for toknum, tokval, start, end, line in self.tokens:
            print(f"Tokenizing: {tokval} (type {toknum}) at {start}-{end}")  # Debug message
            if toknum == tokenize.INDENT or toknum == tokenize.DEDENT:
                continue
            color = self.token_colors.get(tokval, get_color(tokval, self.color_map))
            if toknum == tokenize.STRING:
                color = self.color_map['strings']
            if tokval == '':
                continue
            if tokval.isspace():
                for char in tokval:
                    print(f"Whitespace: {repr(char)} at {start}")  # Debug message
                    colored_tokens.append((char, 'white', start[0]))
            else:
                # Split non-whitespace token by whitespace to include spaces correctly
                parts = []
                current = ""
                for char in tokval:
                    if char.isspace():
                        if current:
                            parts.append((current, color, start[0]))
                            current = ""
                        parts.append((char, 'white', start[0]))
                    else:
                        current += char
                if current:
                    parts.append((current, color, start[0]))
                colored_tokens.extend(parts)
        return colored_tokens

def parse_code_to_tokens(code, color_map):
    tokenizer = CodeTokenizer(code, color_map)
    colored_tokens = tokenizer.get_colored_tokens()

    lines = []
    current_line = []
    current_line_number = 1

    for label, color, line_number in colored_tokens:
        if line_number != current_line_number:
            lines.append(current_line)
            current_line = []
            current_line_number = line_number
        current_line.append(Token(label, color))

    if current_line:
        lines.append(current_line)

    return lines

