def error_message(line_num, error_code, description):
    return f"Line {line_num}: {error_code} {description}"


class Over79CharactersError(Exception):
    def __init__(self, line_num):
        self.message = error_message(line_num, "S001", "Line length over 79 characters")
        super().__init__(self.message)


class IndentationNotMultipleOf4Error(Exception):
    def __init__(self, line_num):
        self.message = error_message(
            line_num, "S002", "Indentation is not a multiple of four"
        )
        super().__init__(self.message)


class UnnecessarySemicolonError(Exception):
    def __init__(self, line_num):
        self.message = error_message(
            line_num, "S003", "Unnecessary semicolon after a statement"
        )
        super().__init__(self.message)


class LessThenTwoSpacesError(Exception):
    def __init__(self, line_num):
        self.message = error_message(
            line_num, "S004", "Less than two spaces before inline comment"
        )
        super().__init__(self.message)


class TodoFoundError(Exception):
    def __init__(self, line_num):
        self.message = error_message(line_num, "S005", "TODO found")
        super().__init__(self.message)


class MoreThanTwoBlankLinesError(Exception):
    def __init__(self, line_num):
        self.message = error_message(
            line_num, "S006", "More than two blank lines preceding a code line"
        )
        super().__init__(self.message)


def line_over_79_characters(line, line_number):
    if len(line.rstrip()) > 79:
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


def main():
    path = input()  # No input prompt allowed lol
    with open(path, "r") as file:
        for n, line in enumerate(file, 1):
            line_over_79_characters(line, n)
            indentation_not_multiple_of_4(line, n)
            unnecessary_semicolon(line, n)


if __name__ == main():
    main()
