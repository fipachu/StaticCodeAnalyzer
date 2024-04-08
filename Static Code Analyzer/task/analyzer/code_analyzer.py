import argparse
import ast
import os
import re

"""Exercise: figure out a way to avoid having multiple functions with the same list of
arguments"""

MUTABLE_LITERAL_NODES = (ast.List, ast.Dict, ast.Set)


class MutableArgumentVisitor(ast.NodeVisitor):
    def __init__(self, path: str):
        self._error_messages: list[tuple[int, str]] = []
        self._path = path

    def visit_FunctionDef(self, node):
        for arg_name, arg_value in zip(node.args.args, node.args.defaults):
            # Check if the default value is a mutable literal type
            if isinstance(arg_value, MUTABLE_LITERAL_NODES):
                # The type checker appears to be wrong about arg_vlue usage
                # noinspection PyTypeChecker
                error_msg = error_message(
                    node.lineno,
                    "S012",
                    f"The default argument '{arg_name.arg}' "
                    f"value {ast.literal_eval(arg_value)} is mutable",
                    self._path,
                )
                self._error_messages.append((node.lineno, error_msg))
                break
        self.generic_visit(node)

    def get_error_messages(self) -> list[tuple[int, str]]:
        return self._error_messages


def error_message(line_num, error_code, description, path: "path to a .py file"):
    return f"{path}: Line {line_num}: {error_code} {description}"


def line_over_79_characters(line, line_number, path):
    if len(line) > 79:
        print(
            error_message(
                line_number, "S001", "Line length over 79 characters", path=path
            )
        )


def indentation_not_multiple_of_4(line, line_number, path):
    indentation = len(line) - len(line.lstrip(" "))
    if indentation % 4 != 0:
        print(
            error_message(
                line_number, "S002", "Indentation is not a multiple of four", path=path
            )
        )


def unnecessary_semicolon(line, line_number, path):
    statement = line.split("#")[0].rstrip()
    if statement and statement[-1] == ";":
        print(
            error_message(
                line_number,
                "S003",
                "Unnecessary semicolon after a statement",
                path=path,
            )
        )


def less_than_2_spaces(line, line_number, path):
    if "#" in line:
        statement = line.split("#")[0]
        if statement and len(statement) - len(statement.rstrip(" ")) < 2:
            print(
                error_message(
                    line_number,
                    "S004",
                    "Less than two spaces before inline comment",
                    path=path,
                )
            )


def todo_found(line, line_number, path):
    if "#" in line:
        comment = line.split("#")[1]
        if "todo" in comment.lower():
            print(error_message(line_number, "S005", "TODO found", path=path))


def more_than_two_blank_lines(line, line_number, blank_count, path):
    if len(line) == 0:
        blank_count += 1
    else:
        if blank_count > 2:
            print(
                error_message(
                    line_number,
                    "S006",
                    "More than two blank lines preceding a code line",
                    path=path,
                )
            )
        blank_count = 0
    return blank_count


def construction_checks(line, line_number, path):
    # noinspection RegExpRepeatedSpace
    match = re.search(
        r"""(def|class)  # Construction name
        (\ +)  # Spaces
        (\w+)  # Class name
        # Optional parent class:
        (?:
            \(
            (\w+)  # Parent class name
            \)
        )?
        (?:\(.*\))?  # Optional arg list for functions
        :  # Match definitions ending in semicolon only""",
        line,
        re.VERBOSE,
    )
    if match:
        construction_name, spaces, object_name, parent = match.groups()

        too_many_spaces_after_construction_name(
            line_number, path, construction_name, spaces
        )
        if construction_name == "class":
            # Not checking the parent. Let's say it should be reported at definition.
            class_name_not_in_camel_case(line_number, path, object_name)
        elif construction_name == "def":
            function_name_not_in_snake_case(line_number, path, object_name)


def too_many_spaces_after_construction_name(
    line_number, path, construction_name, spaces
):
    if len(spaces) > 1:
        print(
            error_message(
                line_number,
                "S007",
                f"Too many spaces after '{construction_name}'",
                path=path,
            )
        )


def class_name_not_in_camel_case(line_number, path, class_name):
    if re.match("[a-z0-9_]+", class_name):
        print(
            error_message(
                line_number,
                "S008",
                f"Class name '{class_name}' should be written in CamelCase",
                path=path,
            )
        )


def is_snake_case(name) -> bool:
    return not re.match("[A-Z]+", name)


def function_name_not_in_snake_case(line_number, path, function_name):
    if not is_snake_case(function_name):
        print(
            error_message(
                line_number,
                "S009",
                f"Function name '{function_name}' should be written in snake_case",
                path=path,
            )
        )


def syntax_tree_checks(tree, path) -> list[tuple[int, str]]:
    # TODO: finnish me!
    # arg_name_errors = argument_name_not_in_snake_case(tree)
    # var_name_errors = variable_name_not_in_snake_case(tree)
    default_arg_errors = mutable_arguments(tree, path)
    return default_arg_errors


def argument_name_not_in_snake_case(line_number, path, argument_name):
    # TODO: rewrite
    if not is_snake_case(argument_name):
        print(
            error_message(
                line_number,
                "S010",
                f"Argument name '{argument_name}' should be written in snake_case",
                path=path,
            )
        )


def variable_name_not_in_snake_case(line_number, path, variable_name):
    # TODO: rewrite
    if not is_snake_case(variable_name):
        print(
            error_message(
                line_number,
                "S011",
                f"Variable name '{variable_name}' should be written in snake_case",
                path=path,
            )
        )


def mutable_arguments(source_code, path) -> list[tuple[int, str]]:
    # Parse the source code into an AST
    tree = ast.parse(source_code)

    # Create an instance of the visitor
    visitor = MutableArgumentVisitor(path)

    # Traverse the AST
    visitor.visit(tree)

    return visitor.get_error_messages()


def analyze_directory(directory):
    for root, _, files in os.walk(directory):
        for name in files:
            path = os.path.join(root, name)

            analyze_file(path)


def analyze_file(path):
    with open(path, "r") as file:
        tree = ast.parse(file.read())
        # IMPORTANT - reset the read pointer:
        file.seek(0)
        errors_from_ast = {}
        for line_num, error in syntax_tree_checks(tree, path):
            if line_num not in errors_from_ast:
                errors_from_ast[line_num] = [error]
            else:
                errors_from_ast[line_num].append(error)
        # print(errors_from_ast)
        # TODO: integrate errors from ast with the rest of errors

        blank_count = 0
        for n, line in enumerate(file, 1):
            line = line.rstrip()

            line_over_79_characters(line, n, path=path)
            indentation_not_multiple_of_4(line, n, path=path)
            unnecessary_semicolon(line, n, path=path)
            less_than_2_spaces(line, n, path=path)
            todo_found(line, n, path=path)
            blank_count = more_than_two_blank_lines(line, n, blank_count, path=path)
            construction_checks(line, n, path=path)
            if n in errors_from_ast:
                for error in errors_from_ast[n]:
                    print(error)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="a valid path to a file or directory")
    file_or_dir = parser.parse_args().path
    # file_or_dir = input()  # No input prompt allowed lol

    if os.path.isdir(file_or_dir):
        analyze_directory(file_or_dir)
    elif os.path.isfile(file_or_dir):
        analyze_file(file_or_dir)


if __name__ == "__main__":
    main()
