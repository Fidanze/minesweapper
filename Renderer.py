from typing import TypeVar
import pygame as pg
from Cell import TCell
import Grid

pg.init()
cFont = pg.font.SysFont('arial', 28)
TRenderer = TypeVar('TRenderer', bound='Renderer')


class Renderer():

    COLORS = {
        1: (0, 0, 255),
        2: (0, 255, 0),
        3: (255, 0, 0),
        4: (0, 0, 128),
        5: (128, 0, 0),
        6: (0, 256, 128),
        7: (0, 0, 0),
        8: (32, 32, 32)}

    def __init__(self: TRenderer, surface: pg.Surface, grid: Grid.TGrid) -> None:
        pg.init()
        self._sc = surface
        self._grid = grid

    @property
    def sc(self: TRenderer):
        return self._sc

    @sc.setter
    def sc(self: TRenderer, new_sc):
        self._sc = new_sc

    @property
    def grid(self: TRenderer):
        return self._grid

    def get_xy(self: TRenderer, coords: tuple[int, int]) -> tuple[int, int]:
        side = self.get_side()
        column: int = coords[0]//side
        row: int = coords[1]//side
        return column, row

    def get_side(self: TRenderer) -> int:
        width: int = self.sc.get_width()
        height: int = self.sc.get_height()

        return min(width//self.grid.columns, height//self.grid.rows)

    def show_cell(self, coords: tuple[int, int] = None, cell: TCell = None) -> None:
        if cell is None:
            cell: TCell = self.grid.get_cell(self.get_xy(coords))
        if not cell.visible:
            cell.visible = True
            if cell not in self.grid.bombs:
                if cell.value == 0:
                    self.show_near_cells(cell)
                    del cell  # lol

    def draw_grid(self) -> None:
        side = self.get_side()
        for cell in self.grid.cells:
            surf = pg.Surface((side, side))
            surf.fill((128, 128, 128), rect=(
                0, 0, int(side*0.9), int(side*0.9)))
            if cell.visible:
                surf.fill((192, 192, 192), rect=(
                    0, 0, int(side*0.9), int(side*0.9)))
                if cell.value in range(1, 9):
                    surf.blit(cFont.render(
                        f'{cell.value}', False, self.COLORS[cell.value]), (side//3, 0))
            self.sc.blit(surf, (cell.column*side, cell.row*side))

    def show_near_cells(self: TRenderer, cell: TCell):
        cross_cells = self.grid.get_around_cells(cell)
        for cross_cell in cross_cells:
            if cross_cell not in self.grid.bombs:
                self.show_cell(cell=cross_cell)
