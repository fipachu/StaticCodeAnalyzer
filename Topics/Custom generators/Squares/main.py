from itertools import count, islice


def squares():
    yield from (i ** 2 for i in count(1))


n = int(input())
for square in islice(squares(), n):
    print(square)
