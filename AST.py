import ast

class NodeVisitor(ast.NodeVisitor):

    def __init__(self):
        self.javaProgram = ""

    def visit_FunctionDef(self, node: ast.FunctionDef):
        lastStatementInBody = node.body[-1]
        if isinstance(lastStatementInBody, ast.Return):
            returnValue = lastStatementInBody.value.value
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


treeWithFunction = ast.parse("""def f():
    y = 1
    return 1
    """)

print(ast.dump(treeWithFunction))
visitor = NodeVisitor()
visitor.visit(treeWithFunction)
print(visitor.javaProgram)


def test_function_returns_integer():
    visitor = NodeVisitor()
    visitor.visit(treeWithFunction)
    assert visitor.javaProgram == "public int f", "Should be: public int f, was " + visitor.javaProgram

if __name__ == "__main__":
    test_function_returns_integer()
    print("Everything ok.")