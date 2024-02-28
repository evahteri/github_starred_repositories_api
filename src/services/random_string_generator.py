import random
import string

class RandomStringGenerator:
    """Generating random strings, used for session secrets in the application.
    Inspiration taken from reference 1 (see README)
    """
    def __init__(self):
        pass

    def generate_random_string(self, length: int) -> str:
        random_string = "".join(random.choices(string.ascii_letters + 
                                               string.digits, k=length))
        return str(random_string)
