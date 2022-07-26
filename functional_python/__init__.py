def pipe(self, *args):
    argsFn = args
    def wrapper(first):
        for fn in argsFn:
            first = fn(first)
        return first

    return wrapper