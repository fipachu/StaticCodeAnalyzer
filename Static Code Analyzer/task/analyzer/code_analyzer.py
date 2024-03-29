class Over79CharactersError(Exception):
    def __init__(self, line_num):
        self.message = f"Line {line_num}: S001 Line length over 79 characters"
        super().__init__(self.message)


def check_for_over_79_characters_error(path):
    with open(path, "r") as file:
        for n, line in enumerate(file, 1):
            try:
                if len(line.rstrip()) > 79:
                    raise Over79CharactersError(n)
            except Over79CharactersError as err:
                print(err)


def main():
    path = input()  # No input prompt allowed lol
    check_for_over_79_characters_error(path)


if __name__ == main():
    main()
