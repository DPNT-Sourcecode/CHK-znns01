# noinspection PyShadowingBuiltins,PyUnusedLocal
def compute(x: int, y: int) -> int:
    if type(x) == int and type(y) == int:
        if (x >= 0 and x <= 100) and (y >= 0 and y <= 100):
            return x + y
        else:
            raise Exception(
                f"Unexpected value for x: {x} or y: {y}."
                " Their value has to be between 0 and 100.")
    else:
        raise Exception(f"Unexpected type for x: {x} or y: {y}.")

