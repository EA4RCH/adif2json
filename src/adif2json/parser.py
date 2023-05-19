from typing import Tuple
from dataclasses import dataclass


@dataclass
class Position:
    remaining: str
    line: int = 1
    column: int = 1


@dataclass
class EndOfFile:
    line: int
    column: int


def discard_until(p: Position, c: str) -> Position | EndOfFile:
    """
    Discard characters from the start of the string until one of the
    characters in chars is found. Return the remaining string.
    It will keep the first character that matches; use discard_forward
    to discard that character as well.
    """
    _, res = read_until(p, c)
    return res


def discard_forward(p: Position, c: str) -> Position | EndOfFile:
    """
    Discard characters from the start of the string until one of the
    characters in chars is found. Return the remaining string.
    It will discard the first character that matches; use discard_until
    to keep that character.
    """
    _, res = read_forward(p, c)
    return res


def read_until(p: Position, c: str) -> Tuple[str, Position | EndOfFile]:
    """
    Read characters from the start of the string until one of the
    characters in chars is found. Return the characters read and the
    remaining string.
    """
    idx = p.remaining.find(c)
    if idx == -1:
        line, col = _update_position(p.remaining, p.line, p.column)
        return p.remaining, EndOfFile(line, col)
    res, rem = read_n(p, idx)
    return res, rem


def read_forward(p: Position, c: str) -> Tuple[str, Position | EndOfFile]:
    """
    Read characters from the start of the string until one of the
    characters in chars is found. Return the characters read and the
    remaining string.
    """
    res, rem = read_until(p, c)
    if isinstance(rem, EndOfFile):
        return res, rem
    line, col = _update_position(rem.remaining[0], rem.line, rem.column)
    p = Position(rem.remaining[1:], line, col)
    return res + rem.remaining[0], p


def _update_position(s: str, line: int, column: int) -> Tuple[int, int]:
    if s == "":
        return line, column
    else:
        if line == 0:
            line = 1
        if column == 0:
            column = 1
    while len(s) > 0:
        if s[0] == "\n":
            line += 1
            column = 0
        else:
            column += 1
        s = s[1:]
    return line, column


def read_n(p: Position, n: int) -> Tuple[str, Position | EndOfFile]:
    """
    Must read n characters from the start of the string. Return the
    characters read and the remaining string.
    """
    if len(p.remaining) < n:
        line, col = _update_position(p.remaining, p.line, p.column)
        return p.remaining, EndOfFile(line, col)
    line, col = _update_position(p.remaining[:n], p.line, p.column)
    return p.remaining[:n], Position(p.remaining[n:], line, col)


def discard_n(p: Position, n: int) -> Position | EndOfFile:
    """
    Must discard n characters from the start of the string. Return the
    remaining string.
    """
    _, res = read_n(p, n)
    return res
