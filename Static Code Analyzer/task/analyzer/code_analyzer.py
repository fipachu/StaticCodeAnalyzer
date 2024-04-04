import argparse
import os
import re

"""Exercise: figure out a way to avoid having multiple functions with the same list of
arguments"""


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
    match = re.search("(def|class)( +)(.+):", line)
    if match:
        construction_name, spaces, object_name = match.groups()

        too_many_spaces_after_construction_name(
            line_number, path, construction_name, spaces
        )


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


def analyze_directory(file_or_dir):
    for root, _, files in os.walk(file_or_dir):
        for name in files:
            path = os.path.join(root, name)

            analyze_file(path)


def analyze_file(path):
    with open(path, "r") as file:
        blank_count = 0
        for n, line in enumerate(file, 1):
            line = line.rstrip()

            line_over_79_characters(line, n, path=path)
            indentation_not_multiple_of_4(line, n, path=path)
            unnecessary_semicolon(line, n, path=path)
            less_than_2_spaces(line, n, path=path)
            todo_found(line, n, path=path)
            blank_count = more_than_two_blank_lines(line, n, blank_count, path=path)


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
