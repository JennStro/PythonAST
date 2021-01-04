import ast

class NodeVisitor(ast.NodeVisitor):
    def visit_Constant(self, node: ast.Constant):
        print("Int " + str(node.s))

    def visit_BinOp(self, node: ast.BinOp):
        print("Binop")
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        returnValue = node.body[0].value.value
        print("public " + str(type(returnValue)) + " " + str(node.name))
        self.generic_visit(node)


simpletree = ast.parse("1 + 2")

NodeVisitor().visit(simpletree)
print(ast.dump(simpletree))


treeWithFunction = ast.parse("""def f(): 
    return 1""")

NodeVisitor().visit(treeWithFunction)
print(ast.dump(treeWithFunction))