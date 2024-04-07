import ast

# put your code here
tree = ast.parse(code)
print(ast.dump(tree))
