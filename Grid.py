from typing import Iterator, TypeVar, Type
from Cell import Cell, TCell
import random
import itertools

AROUND_COORDS_OOFSET = ((-1, -1),
                        (-1, 0),
                        (-1, 1),
                        (0, -1),
                        (0, 1),
                        (1, -1),
                        (1, 0),
                        (1, 1),
                        )

TGrid = TypeVar('TGrid', bound='Grid')


class Grid():
    def __init__(self: TGrid, columns: int = 10, rows: int = 10, bombs: int = 10, torus: bool = False) -> None:
        self.cells = []
        self.columns = columns
        self.rows = rows
        self.bombs = []
        self.torus = torus

        coords = tuple(itertools.product(
            range(self.columns), range(self.rows)))

        for i in range(self.rows*self.columns):
            cell_coords = random.choice(coords)
            while cell_coords in tuple((i.column, i.row) for i in self.cells):
                cell_coords = random.choice(coords)
            if i < bombs:
                cell = Cell(*cell_coords, 9)
                self.cells.append(cell)
                self.bombs.append(cell)
            else:
                self.cells.append(Cell(*cell_coords))

        self.calculate_values()

    def get_cell(self: TGrid, coords) -> TCell | None:
        return tuple(filter(lambda cell: coords == (cell.column, cell.row), self.cells))[0]

    def get_around_cells(self: TGrid, cell: TCell) -> Iterator[TCell]:
        for rel_coords in AROUND_COORDS_OOFSET:
            abs_coords = self.get_coords(cell, rel_coords)
            if abs_coords:
                yield self.get_cell(abs_coords)

    def calculate_values(self: TGrid) -> None:
        for cell in self.bombs:
            around_cells = self.get_around_cells(cell)
            for around_cell in around_cells:
                if around_cell.value != 9:
                    around_cell.value += 1

    def get_coords(self: TGrid, cell: TCell, coords: tuple[int, int]) -> tuple[int, int]:
        column: int = cell.column+coords[0]
        row: int = cell.row+coords[1]
        if self.torus:
            column = (column+self.columns) % self.columns
            row = (row+self.rows) % self.rows
        if column in range(self.columns) and row in range(self.rows):
            return column, row
        else:
            return None

    def isWin(self: TGrid) -> bool:
        unvisible_cells = set(filter(lambda el: not el.visible, self.cells))
        return len(unvisible_cells) == len(self.bombs)

    def isFail(self: TGrid) -> bool:
        return tuple(filter(lambda el: el.visible, self.bombs)) != ()
