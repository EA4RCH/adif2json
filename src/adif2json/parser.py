from typing import Tuple


def discard_until(s: str, *chars: str) -> str:
    """
    Discard characters from the start of the string until one of the
    characters in chars is found. Return the remaining string.
    It will keep the first character that matches; use discard_forward
    to discard that character as well.
    """
    while len(s) > 0:
        if s[0] in chars:
            return s
        s = s[1:]
    return ""


def discard_forward(s: str, *chars: str) -> str:
    """
    Discard characters from the start of the string until one of the
    characters in chars is found. Return the remaining string.
    It will discard the first character that matches; use discard_until
    to keep that character.
    """
    while len(s) > 0:
        if s[0] in chars:
            return s[1:]
        s = s[1:]
    return ""


def read_until(s: str, *chars: str) -> Tuple[str, str]:
    # TODO: implement this function
    return "", ""


def read_n(s: str, n: int) -> Tuple[str, str]:
    # TODO: implement this function
    return "", ""
