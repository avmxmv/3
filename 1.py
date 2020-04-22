for x in range(-10000, 10000):
    if 2 ** (x * x + x - 2) - 2 ** (x * x - 4) == 992:
        print(x)