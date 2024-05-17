import ast

file_path = "load.py"

with open(file_path, "r") as file:
    tree = ast.parse(file.read())
print(type(tree.body[0]) == type(ast.ImportFrom()))
print(ast.dump(tree, indent=2))
print(ast.dump(tree, indent=2))
