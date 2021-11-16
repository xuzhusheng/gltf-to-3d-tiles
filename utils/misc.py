import math
import re


def int_to_bytes(value) -> bytes:
    return value.to_bytes(4, "little")


def padded_len(length, *, padding=4) -> int:
    return math.ceil(length / padding) * padding


CAMEL_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')
CONST_PATTERN = re.compile(r'^([A-Z]|[0-0]|_)*$')


def camel_to_snake(name):
    if CONST_PATTERN.match(name):
        return name

    return CAMEL_PATTERN.sub('_', name).lower()


def snake_to_camel(name):
    if CONST_PATTERN.match(name):
        return name

    name = ''.join(word.title() for word in name.split('_'))
    return name[0].lower() + name[1:]
