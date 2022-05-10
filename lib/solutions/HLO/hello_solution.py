

# noinspection PyUnusedLocal
# friend_name = unicode string
def hello(friend_name: str) -> str:
    if not isinstance(friend_name, str):
        raise Exception(
            f"Unexpected type for {friend_name}."
            " String type expected.")

    return f"Hello, {friend_name}!"
