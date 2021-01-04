import ast

class NodeVisitor(ast.NodeVisitor):
    def visit_Constant(self, node: ast.Constant):
        print("Int " + str(node.s))

    def visit_BinOp(self, node: ast.BinOp):
        print("Binop")
        self.generic_visit(node)

tree = ast.parse("1 + 2")

NodeVisitor().visit(tree)
print(ast.dump(tree))