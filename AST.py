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
                self.javaProgram += "public int " + str(node.name) + " {"
            elif returnType is str:
                self.javaProgram += "public String " + str(node.name) + " {"
            elif returnType is float:
                self.javaProgram += "public double " + str(node.name) + " {"
        else:
            self.javaProgram += "public void " + str(node.name) + " {"

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        value  = node.value.value
        typeOfValue = type(value)
        variableName = node.targets[0].id
        if typeOfValue is int:
            self.javaProgram += "int " + variableName + " = " + str(value) + ";"
        elif typeOfValue is str:
            self.javaProgram += "String " + variableName + " = '" + str(value) + "';"
        elif typeOfValue is float:
            self.javaProgram += "double " + variableName + " = " + str(value) + ";"

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
    functionReturnsInteger = ast.parse("""def f():
    return 1
    """)
    visitor = NodeVisitor()
    visitor.visit(functionReturnsInteger)
    assert visitor.javaProgram == "public int f", "Should be: public int f, was " + visitor.javaProgram

def test_function_returns_string():
    functionReturnsString = ast.parse("""def f():
    return "Hello"
    """)
    visitor = NodeVisitor()
    visitor.visit(functionReturnsString)
    assert visitor.javaProgram == "public String f", "Should be: public String f, was " + visitor.javaProgram

def test_function_returns_void():
    functionReturnsVoid = ast.parse("""def f():
    print("Hello!")
    """)
    visitor = NodeVisitor()
    visitor.visit(functionReturnsVoid)
    assert visitor.javaProgram == "public void f", "Should be: public void f, was " + visitor.javaProgram

def test_assign_integer_variable():
    integerVariable = ast.parse("a = 10")
    visitor = NodeVisitor()
    visitor.visit(integerVariable)
    assert visitor.javaProgram == "int a = 10;", "Should be: int a = 10;, was " + visitor.javaProgram

def test_assign_string_variable():
    stringVariable = ast.parse("a = 'Hei'")
    visitor = NodeVisitor()
    visitor.visit(stringVariable)
    assert visitor.javaProgram == "String a = 'Hei';", "Should be: String a = 'Hei';, was " + visitor.javaProgram

if __name__ == "__main__":
    test_function_returns_integer()
    test_function_returns_string()
    test_function_returns_void()
    test_assign_integer_variable()
    test_assign_string_variable()
    print("Everything ok.")