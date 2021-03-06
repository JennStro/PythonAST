import ast

class NodeVisitor(ast.NodeVisitor):

    def __init__(self):
        self.javaProgram = ""
        self.environment = {}

    def visit_FunctionDef(self, node: ast.FunctionDef):
        lastStatementInBody = node.body[-1]
        arguments = node.args.args

        #print(ast.dump(node))
        #print(ast.dump(node.args))
        #print(arguments)

        #print(self.environment)

        stringWithArguments = ""
        for argument in arguments:
            argumentName = argument.arg
            stringWithArguments += str(self.convertTypeToString(self.environment[argumentName])) + " " + argumentName + ", "

        #Do not want the last ","
        stringWithArguments = stringWithArguments[:-2]

        if isinstance(lastStatementInBody, ast.Return):
            returnValue = lastStatementInBody.value.value
            returnType = type(returnValue)
            if returnType is int:
                self.javaProgram += "public int " + str(node.name)
            elif returnType is str:
                self.javaProgram += "public String " + str(node.name)
            elif returnType is float:
                self.javaProgram += "public double " + str(node.name)
        else:
            self.javaProgram += "public void " + str(node.name)+"(" + stringWithArguments + ")"

        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        value = node.value.value
        typeOfValue = type(value)
        variableName = node.targets[0].id

        self.environment[variableName] = typeOfValue
        #print(self.environment)
        #print(value)
        #self.javaProgram += self.convertTypeToString(typeOfValue) + " " + variableName + " = " + str(value) + ";\n"

        if typeOfValue is int:
            self.javaProgram += "int " + variableName + " = " + str(value) + ";\n"
        elif typeOfValue is str:
            self.javaProgram += "String " + variableName + " = '" + str(value) + "';\n"
        elif typeOfValue is float:
            self.javaProgram += "double " + variableName + " = " + str(value) + ";\n"

        self.generic_visit(node)

    def convertTypeToString(self, theType):
        if theType is int:
            return "int"
        elif theType is str:
            return "String"
        elif theType is float:
            return "double"
        else:
            return "void"

visitor = NodeVisitor()

f = open("test.txt", "r")
visitor.visit(ast.parse(f.read()))
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
    assert visitor.javaProgram == "public void f()", "Should be: public void f, was " + visitor.javaProgram


def test_assign_integer_variable():
    integerVariable = ast.parse("a = 10")
    visitor = NodeVisitor()
    visitor.visit(integerVariable)
    assert visitor.javaProgram == "int a = 10;\n", "Should be: int a = 10;\n, was " + visitor.javaProgram


def test_assign_string_variable():
    stringVariable = ast.parse("a = 'Hei'")
    visitor = NodeVisitor()
    visitor.visit(stringVariable)
    assert visitor.javaProgram == "String a = 'Hei';\n", "Should be: String a = 'Hei';\n, was " + visitor.javaProgram


def test_function_after_assignemnt():
    functionWithNoArgument = ast.parse("x = 1 \ndef f():\n\tprint('Hello world!')")
    visitor = NodeVisitor()
    visitor.visit(functionWithNoArgument)
    assert visitor.javaProgram == "int x = 1;\npublic void f()", "Should be: int x = 1;\npublic void f(), was " + visitor.javaProgram

def test_function_one_argument():
    functionWithOneArgument = ast.parse("x = 1 \ndef f(x):\n\tprint('Hello world!')")
    visitor = NodeVisitor()
    visitor.visit(functionWithOneArgument)
    assert visitor.javaProgram == "int x = 1;\npublic void f(int x)", "Should be: int x = 1;\npublic void f(int x), was " + visitor.javaProgram

def test_function_two_arguments():
    functionWithTwoArguments = ast.parse("x = 1 \ny = 3\ndef f(x, y):\n\tprint('Hello world!')")
    visitor = NodeVisitor()
    visitor.visit(functionWithTwoArguments)
    assert visitor.javaProgram == "int x = 1;\nint y = 3;\npublic void f(int x, int y)", "int x = 1;\nint y = 3;\npublic void f(int x, int y), was " + visitor.javaProgram


if __name__ == "__main__":
    test_function_returns_integer()
    test_function_returns_string()
    test_function_returns_void()
    test_assign_integer_variable()
    test_assign_string_variable()
    test_function_after_assignemnt()
    test_function_one_argument()
    test_function_two_arguments()
    print("Everything ok.")
