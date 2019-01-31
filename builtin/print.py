def printt(args, symbol):
    a = []
    for x in args:
        s = symbol.visit(x)
        a.append(s.value)

    print(*a)
