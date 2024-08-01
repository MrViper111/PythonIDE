import ast
import tokenize
import io
import keyword


# References:
# - https://docs.python.org/3/library/ast.html
# - https://stackoverflow.com/questions/1515357/simple-example-of-how-to-use-ast-nodevisitor
# - https://docs.python.org/3/library/tokenize.html
# - https://thehardcorecoder.com/2021/12/03/python-tokenize/
# - https://pybit.es/articles/ast-intro/
# - Idea to use AST came from Lauren


class Token:
    def __init__(self, label, color):
        self.label = label
        self.color = color

    def __repr__(self):
        return f"Token({self.label!r}, {self.color!r})"


def get_color(token, color_map, context=None):
    context_map = {
        "functions": color_map['functions'],
        "strings": color_map['strings'],
        "comments": color_map['comments']
    }
    if context in context_map:
        return context_map[context]
    if keyword.iskeyword(token):
        return color_map['keywords']
    if token.isidentifier():
        return color_map['variables']
    return 'white'


class CodeTokenizer(ast.NodeVisitor):
    def __init__(self, app, code, color_map):
        self.app = app
        self.color_map = color_map
        self.token_colors = {}
        self.tokens = self.tokenize_code(code)
        self.analyze_ast(code)

    def tokenize_code(self, code):
        tokens = []
        try:
            tokens = list(tokenize.generate_tokens(io.StringIO(code).readline))
            self.app.code_is_invalid = False
        except tokenize.TokenError as e:
            self.app.code_is_invalid = True
            start = e.args[1]
            error_token = code[start[1]:]
            print(f"Token error {start[0]} col {start[1]}: '{error_token}'")
            tokens = self.handle_error_token(code, start)
        return tokens

    def handle_error_token(self, code, start):
        tokens = []
        error_start = start[1]

        # maybe try to tokenize up to error
        try:
            valid_tokens = list(tokenize.generate_tokens(io.StringIO(code[:error_start]).readline))
            tokens.extend(valid_tokens)
        except tokenize.TokenError:
            pass

        # add the error token
        error_token = code[error_start:error_start + 1]  # get the stupid character
        tokens.append((tokenize.ERRORTOKEN, error_token, start, start, code))

        return tokens

    def analyze_ast(self, code):
        try:
            self.visit(ast.parse(code))
        except SyntaxError:
            pass

    def visit_FunctionDef(self, node):
        self.token_colors[node.name] = 'functions'
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.token_colors[node.func.id] = 'functions'
        self.generic_visit(node)

    def visit_Name(self, node):
        self.token_colors.setdefault(node.id, 'variables')
        self.generic_visit(node)

    def visit_Constant(self, node):
        if isinstance(node.value, str):
            self.token_colors[repr(node.value)] = 'strings'
        self.generic_visit(node)

    def get_colored_tokens(self):
        colored_tokens = []
        previous_end = None
        current_line = 1
        current_col = 0

        for token_num, token_value, start, end, _ in self.tokens:
            start_line, start_col = start
            if token_num in (tokenize.NEWLINE, tokenize.NL):
                colored_tokens.append(Token("\n", "white"))
                current_line += 1
                current_col = 0
                continue
            if token_num in (tokenize.INDENT, tokenize.DEDENT):
                for char in token_value:
                    if char == " ":
                        colored_tokens.append(Token(" ", "white"))
                        current_col += 1
                    elif char == "\t":
                        colored_tokens.append(Token("\t", "white"))
                        current_col += 1
                continue
            if start_line > current_line:
                colored_tokens.append(Token("\n", "white"))
                current_line = start_line
                current_col = 0
            while start_col > current_col:
                colored_tokens.append(Token(" ", "white"))
                current_col += 1
            color = self.get_token_color(token_num, token_value)
            if token_num == tokenize.ERRORTOKEN:
                colored_tokens.append(Token(token_value, "white"))
                break
            else:
                colored_tokens.append(Token(token_value, color))
                current_col += len(token_value)
        return colored_tokens

    def get_token_color(self, token_num, token_value):
        if token_num == tokenize.COMMENT:
            return self.color_map["comments"]
        if token_num == tokenize.ERRORTOKEN:
            return "white"
        if token_num == tokenize.STRING:
            return self.color_map["strings"]
        context = self.token_colors.get(token_value)
        return get_color(token_value, self.color_map, context)


def parse_code_to_tokens(app, code, color_map):
    tokenizer = CodeTokenizer(app, code, color_map)
    colored_tokens = tokenizer.get_colored_tokens()

    lines = []
    current_line = []

    for token in colored_tokens:
        if token.label == "\n":
            lines.append(current_line)
            current_line = []
        else:
            current_line.append(token)

    if current_line:
        lines.append(current_line)

    return lines

