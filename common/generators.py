import random
# maximum length of password needed
# this can be changed to suit your password length
from functools import reduce
from uuid import uuid4

MAX_LEN = 30

# declare arrays of the character that we need in out password
# Represented as chars to enable easy string concatenation
DIGITS = "0123456789"
LOW_CASE_CHARACTERS = "abcdefghijkmnopqrstuvwxyz"
UP_CASE_CHARACTERS = "ABCDEFGHIJKMNOPQRSTUVWXYZ"
SPECIAL_CHARACTERS = "!()-.?[]_`~;:@#$%^&*+="

# combines all the character arrays above to form one array
CHARACTER_LIST = [DIGITS, LOW_CASE_CHARACTERS, UP_CASE_CHARACTERS, SPECIAL_CHARACTERS]


def password_generator():
    return ''.join(random.sample(
        random.sample(reduce(lambda a, b: a + b, CHARACTER_LIST), MAX_LEN - len(CHARACTER_LIST)) +
        [random.choice(chars) for chars in CHARACTER_LIST],
        MAX_LEN
    ))


def email_generator():
    return f"m{uuid4()}@email.com".replace("-", "")
