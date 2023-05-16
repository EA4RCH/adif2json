from typing import Tuple, Optional
from itertools import islice


def discard_until(s: str, *chars: str) -> Optional[str]:
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
    return None


def discard_forward(s: str, *chars: str) -> Optional[str]:
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
    return None


def read_until(s: str, *chars: str) -> Optional[Tuple[str, str]]:
    """
    Read characters from the start of the string until one of the
    characters in chars is found. Return the characters read and the
    remaining string.
    """
    res = ""
    while len(s) > 0:
        if s[0] in chars:
            return res, s
        res += s[0]
        s = s[1:]
    return None


def read_forward(s: str, *chars: str) -> Optional[Tuple[str, str]]:
    """
    Read characters from the start of the string until one of the
    characters in chars is found. Return the characters read and the
    remaining string.
    """
    res = ""
    while len(s) > 0:
        res += s[0]
        if s[0] in chars:
            return res, s[1:]
        s = s[1:]
    return None


def read_n(s: str, n: int) -> Tuple[str, str]:
    """
    Must read n characters from the start of the string. Return the
    characters read and the remaining string.
    The characters can be unicode characters, so we can't just use
    s[:n] to get the characters.
    """
    s_iter = iter(s)
    first_n_chars = ''.join(islice(s_iter, n))
    remaining_chars = ''.join(s_iter)
    return first_n_chars, remaining_chars
