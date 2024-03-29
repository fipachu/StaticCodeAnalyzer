def error_message(line_num, error_code, description):
    return f"Line {line_num}: {error_code} {description}"


def line_over_79_characters(line, line_number):
    if len(line) > 79:
        print(error_message(line_number, "S001", "Line length over 79 characters"))


def indentation_not_multiple_of_4(line, line_number):
    indentation = len(line) - len(line.lstrip(" "))
    if indentation % 4 != 0:
        print(
            error_message(line_number, "S002", "Indentation is not a multiple of four")
        )


def unnecessary_semicolon(line, line_number):
    statement = line.split("#")[0].rstrip()
    if statement and statement[-1] == ";":
        print(
            error_message(
                line_number, "S003", "Unnecessary semicolon after a statement"
            )
        )


def less_than_2_spaces(line, line_number):
    if "#" in line:
        statement = line.split("#")[0]
        if statement and len(statement) - len(statement.rstrip(" ")) < 2:
            print(
                error_message(
                    line_number, "S004", "Less than two spaces before inline comment"
                )
            )


def todo_found(line, line_number):
    if "#" in line:
        comment = line.split("#")[1]
        if "todo" in comment.lower():
            print(error_message(line_number, "S005", "TODO found"))


def more_than_two_blank_lines(line, line_number, blank_count):
    if len(line) == 0:
        blank_count += 1
    else:
        if blank_count > 2:
            print(
                error_message(
                    line_number,
                    "S006",
                    "More than two blank lines preceding a code line",
                )
            )
        blank_count = 0
    return blank_count


def main():
    path = input()  # No input prompt allowed lol
    with open(path, "r") as file:
        blank_count = 0
        for n, line in enumerate(file, 1):
            line = line.rstrip()

            line_over_79_characters(line, n)
            indentation_not_multiple_of_4(line, n)
            unnecessary_semicolon(line, n)
            less_than_2_spaces(line, n)
            todo_found(line, n)
            blank_count = more_than_two_blank_lines(line, n, blank_count)


if __name__ == main():
    main()
