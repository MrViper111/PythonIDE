import ast


# Resources to create these classes came from:
# - https://docs.python.org/3/library/ast.html#
# - https://stackoverflow.com/questions/1515357/simple-example-of-how-to-use-ast-nodevisitor

class ASTHelper:

    @staticmethod
    def get_ast_rep(code: str):
        try:
            return ast.parse(code)
        except SyntaxError:
            return None

    @staticmethod
    def load_ast_data(ast_data):
        if ast_data is None:
            return {"func": set(), "var": set()}

        visitor = AstVisitor()
        visitor.visit(ast_data)
        return {"func": visitor.functions, "var": visitor.variables}


class AstVisitor(ast.NodeVisitor):

    def __init__(self):
        self.functions = set()
        self.variables = set()

    def visit_FunctionDef(self, node):
        self.functions.add(node.name)
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            self.functions.add(node.func.id)

        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.variables.add(target.id)

        self.generic_visit(node)
