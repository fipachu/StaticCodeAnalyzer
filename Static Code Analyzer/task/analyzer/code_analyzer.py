path = input()  # No input prompt allowed lol
with open(path, 'r') as file:
    for n, line in enumerate(file, 1):
        # print(f'line #{n}: {repr(line)}')
        if len(line.rstrip()) > 79:
            print(f'Line {n}: S001 Line length over 79 characters')
