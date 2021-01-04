import ast

class NodeVisitor(ast.NodeVisitor):
    def visit_Constant(self, node: ast.Constant):
        print(str(node.s))

    def visit_BinOp(self, node: ast.BinOp):
        print("Binop")
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        returnValue = node.body[0].value.value
        returnType = type(returnValue)
        print(returnType)
        if returnType is int:
            print("public int " + str(node.name))
        elif returnType is str:
            print("public String " + str(node.name))
        elif returnType is float:
            print("public double " + str(node.name))
        else:
            print("public void " + str(node.name))

        self.generic_visit(node)


simpletree = ast.parse("1 + 2")

NodeVisitor().visit(simpletree)
print(ast.dump(simpletree))


treeWithFunction = ast.parse("""def f():
    return 'helo'
    """)

NodeVisitor().visit(treeWithFunction)
print(ast.dump(treeWithFunction))