import ast

tree = ast.parse("1 + 2")

print(ast.dump(tree))