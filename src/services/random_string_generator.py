import random
import string

class RandomStringGenerator:
    """Generating random strings, used for session secrets in the application.
    Inspiration taken from reference 1 (see README)
    """
    def __init__(self):
        pass

    def generate_random_string(self, length: int) -> str:
        if length <= 0:
            raise ValueError("The length of the random string must be a positive integer.")
        random_string = "".join(random.choices(string.ascii_letters + 
                                               string.digits, k=length))
        return str(random_string)
