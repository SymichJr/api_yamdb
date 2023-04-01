import random
import string


def generate_token(length=100):
    return "".join(
        random.choices(string.ascii_letters + string.digits, k=length)
    )

