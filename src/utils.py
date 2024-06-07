import random
import string


def random_string(length=8, choices=string.ascii_lowercase + string.digits):
    return ''.join(random.choices(choices, k=length))


def random_email():
    random_user = random_string(1, string.ascii_lowercase) + random_string(6)
    random_domain = random_string(1, string.ascii_lowercase) + random_string(4)
    random_domain_level_one = random_string(1, string.ascii_lowercase) + random_string(1)
    return f'{random_user}@{random_domain}.{random_domain_level_one}'
