import ast

tree = ast.parse(code)

# put your code here
EXAMPLE = """
import random
import time

print("Welcome to the Random Number Generator!")

for _ in range(10):
    random_number = random.randint(1, 10)
    print(f"Random number is: {random_number}")
    time.sleep(2)"""
# tree = ast.parse(EXAMPLE)


class ImportVisitor(ast.NodeVisitor):
    def visit_Import(self, node):
        # print(node.names)
        for alias in node.names:
            print(alias.name)


ImportVisitor().visit(tree)