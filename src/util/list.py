def flatMap(f, xs):
    return (y for ys in xs for y in f(ys))
