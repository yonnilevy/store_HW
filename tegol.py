def tegol_1():
    a = [x if x % 7 else "Boom" for x in range(1, 22)]
    print(a)
    b = [x for x in (80, 83)]
    c = {chr(x): x for x in range(80, 83)}
    print(c)
    start, *mid, end = list(range(0,10,2))
    print(f"{start}, {mid}, {end}")


if __name__ == '__main__':
    print('PyCharm')
    tegol_1()
