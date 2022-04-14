from Cell import Cell
from Grid import Grid
from Renderer import Renderer
import pygame as pg


# здесь определяются константы, классы и функции
pg.init()
FPS = 60
BLACK = (0, 0, 0)
cFont = pg.font.SysFont('arial', 28)


def main():
    grid = Grid(25, 15, 50, True)
    cScreen = pg.display.set_mode((960, 540), pg.RESIZABLE)
    while True:
        run(grid, cScreen)


def run(grid, cScreen):
    gui_renderer = Renderer(cScreen, grid)
    while True:
        # gui_renderer.clock.tick(FPS)
        # цикл обработки событий
        event_list = pg.event.get()
        if event_list:
            for i in event_list:
                # события выхода
                if i.type == pg.QUIT:
                    exit()
                # ЛКМ
                if i.type == pg.MOUSEBUTTONDOWN:
                    if i.button == 1:
                        gui_renderer.show_cell(coords=i.pos)
                    elif i.button == 3:
                        exit()
                    else:
                        pass
        gui_renderer.draw_grid()
        pg.display.update()
        if gui_renderer.grid.isFail():
            print('You lose!')
            exit()
        if gui_renderer.grid.isWin():
            print('You win!')
            exit()


if __name__ == '__main__':
    main()
