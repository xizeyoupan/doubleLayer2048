# @Project_name:2048
# @Author : LKY
# @File : main.py
# @Software: PyCharm

import random
import pygame
from pygame.locals import *
from sys import exit

COLOURS = {'WHITE': (255, 255, 255), 'FONT': (119, 110, 101), '': (205, 193, 180), '1': (250, 248, 239),
           '2': (238, 228, 218), '4': (237, 224, 200), '8': (242, 177, 121), '16': (245, 149, 99), '32': (246, 124, 95),
           '64': (242, 93, 58), '128': (237, 207, 114), '256': (208, 246, 82),
           'ELSE': (135, 226, 255)}


class Game2i2(object):
    def __init__(self):
        self.blank_block = []
        self.map_main = {}
        self.map_pic = '''
    ------------------------------------------------------------|
    |               |               |             |             |
    |        a      |      b        |       c     |     d       |
    |       {}       |      {}        |         {}   |     {}       |
    |               |               |             |             |
    | --------------|-------|-------|------|------|-------------|
    |               |    f  |  g    |  h   |   i  |             |
    |        e      |__{}____|____{}__|___{}__|___{}__|     n       |
    |      {}        |   j   |   k   |   l  |   m  |     {}       |
    |               |   {}   |   {}   |    {} |   {}  |             |
    | --------------|-------|-------|------|------|-------------|
    |               |   p   |   q   |   r  |   s  |             |
    |        o      |   {}   |   {}   |    {} |   {}  |      x      |
    |        {}      |-------|-------|------|------|     {}       |
    |               |    t  |  u    |  v   |   w  |             |
    |_______________|____{}__|____{}__|___{}__|___{}__|_____________|
    |               |               |             |             |
    |        y      |      z        |      yy     |    zz       |
    |         {}     |      {}        |         {}   |      {}      |
    |               |               |             |             |
    | --------------|---------------|-------------|-------------|
'''
        self.isend = False
        self.score = 0

    def update_blank(self):  # call this after change map
        self.blank_block = []
        for key, value in self.map_main.items():
            if value == 0:
                self.blank_block.append(key)

    def new_game(self):
        self.map_main = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0, 'g': 0, 'h': 0, 'i': 0, 'j': 0, 'k': 0, 'l': 0,
                         'm': 0, 'n': 0,
                         'o': 0, 'p': 0, 'q': 0, 'r': 0, 's': 0, 't': 0, 'u': 0, 'v': 0, 'w': 0, 'x': 0, 'y': 0, 'z': 0,
                         'yy': 0, 'zz': 0}
        new_key = random.sample(self.map_main.keys(), 2)
        for i in new_key:  # 开始的两个方块数字均为二
            self.map_main[i] = 2
        self.update_blank()

    def chcek(self):
        self.isend = True
        for i in (['a', 'b', 'c', 'd'], ['y', 'z', 'yy', 'zz'], ['f', 'g', 'h', 'i'], ['j', 'k', 'l', 'm'],
                  ['p', 'q', 'r', 's'],
                  ['t', 'u', 'v', 'w'], ['a', 'e', 'o', 'y'], [
                      'd', 'n', 'x', 'zz'], ['f', 'j', 'p', 't'],
                  ['g', 'k', 'q', 'u'], ['h', 'l', 'r', 'v'], ['i', 'm', 's', 'w']):
            for j_index, j in enumerate(i[:-1]):
                if self.map_main[i[j_index]] == 0 or self.map_main[i[j_index]] == self.map_main[i[j_index + 1]]:
                    self.isend = False

        if self.isend:
            self.game_over()

    def add_blcok(self):
        block_value = 2 if random.choice(range(4)) == 0 else 4
        block_key = random.choice(self.blank_block)
        self.map_main[block_key] = block_value
        self.update_blank()

    def game_over(self):
        print('game_over!!')

    def show(self):
        print('your score:{}'.format(self.score))
        print(self.map_pic.format(self.map_main['a'], self.map_main['b'], self.map_main['c'], self.map_main['d'],
                                  self.map_main['f'], self.map_main['g'], self.map_main['h'], self.map_main['i'],
                                  self.map_main['e'], self.map_main['n'], self.map_main['j'], self.map_main['k'],
                                  self.map_main['l'], self.map_main['m'], self.map_main['p'], self.map_main['q'],
                                  self.map_main['r'], self.map_main['s'], self.map_main['o'], self.map_main['x'],
                                  self.map_main['t'], self.map_main['u'], self.map_main['v'], self.map_main['w'],
                                  self.map_main['y'], self.map_main['z'], self.map_main['yy'], self.map_main['zz']))

    # [a,b,c,d],[dgseg].
    def _move_and_calculate(self, first_block=None, last_block=None, *args):
        # 先都移动到一边（冒泡的方式）
        kwargs = {}
        for i in args:
            for j in i:
                kwargs[j] = self.map_main[j]

        def _move(*args, **kwargs):
            for t in args:
                for j in range(3):
                    for index, i in enumerate(t[:-1]):
                        if kwargs[t[index]] == 0:
                            kwargs[t[index]], kwargs[t[index + 1]
                                                     ] = kwargs[t[index + 1]], kwargs[t[index]]
            return args, kwargs

        def _calculate(*args, **kwargs):
            for i in args:
                for key_index, key in enumerate(i[:-1]):
                    if kwargs[key] != 0 and kwargs[key] == kwargs[i[key_index + 1]]:
                        kwargs[key] *= 2
                        kwargs[i[key_index + 1]] = 0
                        self.score += kwargs[key]

            args, kwargs = _move(*args, **kwargs)
            return args, kwargs

        args, kwargs = _move(*args, **kwargs)

        if first_block and last_block:
            # 处理第一个
            if (kwargs[args[0][0]] == kwargs[args[1][0]] and first_block[1] == 2 * kwargs[args[0][0]]) or \
                    (first_block[1] == 0 and kwargs[args[0][0]] == kwargs[args[1][0]]):
                first_block[1] += 2 * kwargs[args[0][0]]
                self.score += first_block[1]
                kwargs[args[0][0]], kwargs[args[1][0]] = 0, 0
                args, kwargs = _move(*args, **kwargs)
                args, kwargs = _calculate(*args, **kwargs)

            args, kwargs = _calculate(*args, **kwargs)
            # 处理第二个
            if (kwargs[args[0][-1]], kwargs[args[1][-1]]) == (0, 0):  # 两个都是零的情况
                kwargs[args[0][-1]], kwargs[args[1][-1]
                                            ] = last_block[1] // 2, last_block[1] // 2
                last_block[1] = 0
            elif kwargs[args[0][-1]] == kwargs[args[1][-1]] and kwargs[args[0][-1]] == last_block[
                    1] // 2:  # 两个都是那个数除以二的情况
                kwargs[args[0][-1]], kwargs[args[1][-1]
                                            ] = kwargs[args[0][-1]] * 2, kwargs[args[1][-1]] * 2
                last_block[1] = 0
            elif (kwargs[args[0][-1]], kwargs[args[1][-1]]) == (0, last_block[1] // 2):
                kwargs[args[0][-1]], kwargs[args[1][-1]
                                            ] = last_block[1] // 2, kwargs[args[1][-1]] * 2
                last_block[1] = 0
            elif (kwargs[args[0][-1]], kwargs[args[1][-1]]) == (last_block[1] // 2, 0):
                kwargs[args[0][-1]], kwargs[args[1][-1]
                                            ] = kwargs[args[1][-1]] * 2, last_block[1] // 2
                last_block[1] = 0
            args, kwargs = _move(*args, **kwargs)
        else:
            args, kwargs = _calculate(*args, **kwargs)

        for key, value in kwargs.items():
            self.map_main[key] = value

        if first_block and last_block:
            self.map_main[first_block[0]] = first_block[1]
            self.map_main[last_block[0]] = last_block[1]

        self.update_blank()
        self.chcek()

    def move_to_left(self):
        kws = self.map_main.copy()
        self._move_and_calculate(None, None, ['a', 'b', 'c', 'd'], [
                                 'y', 'z', 'yy', 'zz'])
        self._move_and_calculate(['e', self.map_main['e']], ['n', self.map_main['n']], ['f', 'g', 'h', 'i'],
                                 ['j', 'k', 'l', 'm'])
        self._move_and_calculate(['o', self.map_main['o']], ['x', self.map_main['x']], ['p', 'q', 'r', 's'],
                                 ['t', 'u', 'v', 'w'])
        if kws != self.map_main:
            self.add_blcok()

    def move_to_right(self):
        kws = self.map_main.copy()
        self._move_and_calculate(None, None, ['d', 'c', 'b', 'a'], [
                                 'zz', 'yy', 'z', 'y'])
        self._move_and_calculate(['n', self.map_main['n']], ['e', self.map_main['e']], ['i', 'h', 'g', 'f'],
                                 ['m', 'l', 'k', 'j'])
        self._move_and_calculate(['x', self.map_main['x']], ['o', self.map_main['o']], ['s', 'r', 'q', 'p'],
                                 ['w', 'v', 'u', 't'])
        if kws != self.map_main:
            self.add_blcok()

    def move_to_up(self):
        kws = self.map_main.copy()
        self._move_and_calculate(None, None, ['a', 'e', 'o', 'y'], [
                                 'd', 'n', 'x', 'zz'])
        self._move_and_calculate(['b', self.map_main['b']], ['z', self.map_main['z']], ['f', 'j', 'p', 't'],
                                 ['g', 'k', 'q', 'u'])
        self._move_and_calculate(['c', self.map_main['c']], ['yy', self.map_main['yy']], ['h', 'l', 'r', 'v'],
                                 ['i', 'm', 's', 'w'])
        if kws != self.map_main:
            self.add_blcok()

    def move_to_down(self):
        kws = self.map_main.copy()
        self._move_and_calculate(None, None, ['y', 'o', 'e', 'a'], [
                                 'zz', 'x', 'n', 'd'])
        self._move_and_calculate(['z', self.map_main['z']], ['b', self.map_main['b']], ['t', 'p', 'j', 'f'],
                                 ['u', 'q', 'k', 'g'])
        self._move_and_calculate(['yy', self.map_main['yy']], ['c', self.map_main['c']], ['v', 'r', 'l', 'h'],
                                 ['w', 's', 'm', 'i'])
        if kws != self.map_main:
            self.add_blcok()


class GameGUI(Game2i2):
    def __init__(self):
        super(GameGUI, self).__init__()
        pygame.init()
        SCREEN_SIZE = (640, 960)
        self.screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)

    def text_display(self, text, on_surface, font_size, font_color, bk_color=None, font='arial'):
        if text == '0':
            text = ''
        fontObj = pygame.font.SysFont(font, font_size)
        textSurfaceObj = fontObj.render(text, True, font_color, bk_color)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = on_surface.get_rect().center
        if text in COLOURS.keys():
            on_surface.fill(COLOURS[text])
        else:
            on_surface.fill(COLOURS['ELSE'])
        on_surface.blit(textSurfaceObj, textRectObj)

    def game_over(self):
        butm = pygame.image.load('butm.jpg')
        fontObj = pygame.font.Font('fzst.ttf', 30)
        textSurfaceObj = fontObj.render(
            '游戏结束！！！总分{}'.format(self.score), True, (0, 0, 0), None)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (273, 28)
        butm.blit(textSurfaceObj, textRectObj)
        self.screen.blit(butm, (0, 640))

    def main(self):
        self.new_game()
        pygame.display.set_caption('2048in2048')
        playbkgd = pygame.image.load('2048bkgd.png')

        def send_score():
            if self.isend:
                self.game_over()
                return
            fontObj = pygame.font.Font('fzst.ttf', 30)
            textSurfaceObj = fontObj.render(
                '你的得分:{}'.format(self.score), True, (0, 0, 0), None)
            textRectObj = textSurfaceObj.get_rect()
            butm = pygame.image.load('butm.jpg')
            butm.blit(textSurfaceObj, textRectObj)
            self.screen.blit(butm, (0, 640))

        def display():
            for index, i in enumerate(['a', 'b', 'c', 'd']):
                self.text_display(
                    str(self.map_main[i]), big_block, 50, COLOURS['FONT'])
                self.screen.blit(big_block, (5 + index * (150 + 10), 5))

            for index, i in enumerate(['e', 'o', 'y']):
                self.text_display(
                    str(self.map_main[i]), big_block, 50, COLOURS['FONT'])
                self.screen.blit(big_block, (5, 165 + index * (150 + 10)))

            for index, i in enumerate(['z', 'yy', 'zz']):
                self.text_display(
                    str(self.map_main[i]), big_block, 50, COLOURS['FONT'])
                self.screen.blit(big_block, (165 + index * (150 + 10), 485))

            for index, i in enumerate(['n', 'x']):
                self.text_display(
                    str(self.map_main[i]), big_block, 50, COLOURS['FONT'])
                self.screen.blit(big_block, (485, 165 + index * 160))

            for j_index, j in enumerate(
                    [['f', 'g', 'h', 'i'], ['j', 'k', 'l', 'm'], ['p', 'q', 'r', 's'], ['t', 'u', 'v', 'w']]):
                for i_index, i in enumerate(j):
                    self.text_display(
                        str(self.map_main[i]), small_block, 50, COLOURS['FONT'])
                    self.screen.blit(
                        small_block, (165 + 78 * i_index, 165 + 78 * j_index))

        send_score()
        big_block_rect = Rect(0, 0, 150, 150)
        blockimg = pygame.image.load('2048whitebkgd.png')
        big_block = blockimg.subsurface(big_block_rect)
        small_block_rect = Rect(165, 165, 75, 75)
        small_block = blockimg.subsurface(small_block_rect)
        self.screen.blit(playbkgd, (0, 0))
        display()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()
                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_a:
                        self.move_to_left()
                    elif event.key == pygame.K_w:
                        self.move_to_up()
                    elif event.key == pygame.K_s:
                        self.move_to_down()
                    elif event.key == pygame.K_d:
                        self.move_to_right()
                    display()
                    # self.show()
                    send_score()

            pygame.display.update()


if __name__ == '__main__':
    mygui = GameGUI()
    mygui.new_game()
    mygui.main()
