import ast

class NodeVisitor(ast.NodeVisitor):

    def __init__(self):
        self.javaProgram = ""

    def visit_Constant(self, node: ast.Constant):
        print(str(node.s))

    def visit_FunctionDef(self, node: ast.FunctionDef):
        returnValue = node.body[0].value.value
        returnType = type(returnValue)
        print(returnType)
        if returnType is int:
            self.javaProgram += "public int " + str(node.name)
        elif returnType is str:
            self.javaProgram += "public String " + str(node.name)
        elif returnType is float:
            self.javaProgram += "public double " + str(node.name)
        else:
            self.javaProgram += "public void " + str(node.name)

        self.generic_visit(node)



simpletree = ast.parse("1 + 2")

print(ast.dump(simpletree))
NodeVisitor().visit(simpletree)




treeWithFunction = ast.parse("""def f():
    return 1
    """)

print(ast.dump(treeWithFunction))
visitor = NodeVisitor()
visitor.visit(treeWithFunction)
print(visitor.javaProgram)