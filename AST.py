import ast

class NodeVisitor(ast.NodeVisitor):
    def visit_Constant(self, node: ast.Constant):
        print("Int " + str(node.s))

tree = ast.parse("1 + 2")

NodeVisitor().visit(tree)
print(ast.dump(tree))