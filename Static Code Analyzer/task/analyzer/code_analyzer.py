class Over79CharactersError(Exception):
    def __init__(self, line_num):
        self.message = f"Line {line_num}: S001 Line length over 79 characters"
        super().__init__(self.message)


def main():
    path = input()  # No input prompt allowed lol
    with open(path, "r") as file:
        for n, line in enumerate(file, 1):
            try:
                if len(line.rstrip()) > 79:
                    raise Over79CharactersError(n)
            except Over79CharactersError as err:
                print(err)


if __name__ == main():
    main()
