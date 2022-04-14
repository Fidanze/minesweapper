import random
import itertools
from typing import Type, TypeVar
from pygame import Surface


TCell = TypeVar('TCell', bound='Cell')


class Cell:

    def __init__(self: TCell, column: int, row: int, value: int = 0) -> None:
        self._column: int = column
        self._row: int = row
        self._value: int = value
        self._visible: bool = False

    @property
    def column(self: TCell):
        return self._column

    @column.setter
    def column(self: TCell, column: int):
        self._column = column

    @property
    def row(self: TCell):
        return self._row

    @row.setter
    def row(self: TCell, row: int):
        self._row = row

    @property
    def value(self: TCell):
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = value

    @property
    def visible(self: TCell):
        return self._visible

    @visible.setter
    def visible(self: TCell, visible: bool):
        self._visible = visible

    def get_coords(self: TCell, coords: tuple[int, int], torus: bool) -> tuple[int, int]:
        if torus:
            return self.column+coords[0], self.row+coords[1]
        else:
            return abs(self.column+coords[0]), abs(self.row+coords[1])
