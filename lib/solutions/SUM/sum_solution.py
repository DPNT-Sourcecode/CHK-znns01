# noinspection PyShadowingBuiltins,PyUnusedLocal
def compute(x: int, y: int) -> int:
    if type(x) == int and type(y) == int:
        return x + y
    else:
        raise Exception(f"Unexpected type for x: {x} or y: {y}.")


