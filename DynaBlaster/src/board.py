import numpy as np
import random

from src import constants as const
from src import player
from src import monster


class Board(object):

    def __init__(self, players):

        self.width = const.BOARD_WIDTH
        self.height = const.BOARD_HEIGHT
        self.tiles = np.zeros((self.width, self.height), dtype=int)

        self.players = players
        self.player_1 = player.Player('Player 1', 1, 1)
        self.player_2 = player.Player('Player 2', 17, 17)

        self.monster_1 = monster.Monster('Monster 1', random.randint(2,16), random.randint(2,16))
        self.monster_2 = monster.Monster('Monster 2', random.randint(2, 16), random.randint(2, 16))
        self.monster_3 = monster.Monster('Monster 3', random.randint(2, 16), random.randint(2, 16))


        self.create_board()
        self.board_history = []

        for x in range(self.width):
            for y in range(self.height):
                    move = '@' + str(x) + '*' + str(y) + '*' + str(self.tiles[x, y]) + '*!'
                    self.board_history.append(move)
        self.board_history.append('#')

    def create_board(self):

        for i in range(self.width):
            for j in range(self.height):
                self.tiles[i, j] = const.WALL

        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                self.tiles[i, j] = const.GRASS

        for i in range(1, self.width - 1):
            for j in range(1, self.height - 1):
                self.tiles[i, j] = random.randint(const.GRASS, const.WOOD)

        self.tiles[2::2, ::2] = const.WALL

        if self.players == 1:
            for k in [0, 1, 2]:
                if self.tiles[1, k] != const.WALL:
                    self.tiles[1, k] = const.GRASS
            for k in [0, 1, 2]:
                if self.tiles[k, 1] != const.WALL:
                    self.tiles[k, 1] = const.GRASS
            self.tiles[self.player_1.get_pos_x(), self.player_1.get_pos_y()] = const.PLAYER_FRONT

            for k in [16, 17, 18]:
                if self.tiles[17, k] != const.WALL:
                    self.tiles[17, k] = const.GRASS
            for k in [16, 17, 18]:
                if self.tiles[k, 17] != const.WALL:
                    self.tiles[k, 17] = const.GRASS
            self.tiles[self.player_2.get_pos_x(), self.player_2.get_pos_y()] = const.PLAYER_FRONT2

        if self.players == 2:
            for i, j in ([1, 1], [self.width - 2, self.height - 2]):
                for k in [j - 1, j, j + 1]:
                    if self.tiles[i, k] != const.WALL:
                        self.tiles[i, k] = const.GRASS
                for k in [i - 1, i, i + 1]:
                    if self.tiles[k, j] != const.WALL:
                        self.tiles[k, j] = const.GRASS
                self.tiles[i, j] = const.PLAYER_FRONT

        if self.players == 3:
            p = 3
            for i in [1, self.width - 2]:
                for j in [self.height - 2, 1]:
                    if p != 0:
                        for k in [j - 1, j, j + 1]:
                            if self.tiles[i, k] != const.WALL:
                                self.tiles[i, k] = const.GRASS
                        for k in [i - 1, i, i + 1]:
                            if self.tiles[k, j] != const.WALL:
                                self.tiles[k, j] = const.GRASS
                        self.tiles[i, j] = const.PLAYER_FRONT
                        p -= 1

        if self.players >= 4:
            for i in [1, self.width - 2]:
                for j in [1, self.height - 2]:
                    for k in [j - 1, j, j + 1]:
                        if self.tiles[i, k] != const.WALL:
                            self.tiles[i, k] = const.GRASS
                    for k in [i - 1, i, i + 1]:
                        if self.tiles[k, j] != const.WALL:
                            self.tiles[k, j] = const.GRASS
                    self.tiles[i, j] = const.PLAYER_FRONT

        ########


        self.tiles[self.monster_1.get_pos_x(),self.monster_1.get_pos_y()] = const.MONSTER
        self.tiles[self.monster_2.get_pos_x(), self.monster_2.get_pos_y()] = const.MONSTER
        self.tiles[self.monster_3.get_pos_x(), self.monster_3.get_pos_y()] = const.MONSTER

    def save_change(self, previous_board):

        for x in range(self.width):
            for y in range(self.height):
                if previous_board[x, y] != self.tiles[x, y]:
                    move = '@' + str(x) + '*' + str(y) + '*' + str(self.tiles[x, y]) + '*!'
                    self.board_history.append(move)

        self.board_history.append('#')

    def try_move(self, x, y):

        if self.tiles[x, y] != const.WALL and self.tiles[x, y] != const.WOOD and self.tiles[x, y] != const.BOMB:
            return True
        else:
            return False

    def try_moveM(self, x, y):

        if self.tiles[x, y] != const.WALL and self.tiles[x, y] != const.WOOD and self.tiles[x, y] != const.BOMB and self.tiles[x, y] != const.MONSTER :
            return True
        else:
            return False

    def move(self, x, y, p):
        if(p == 1):

            if self.tiles[self.player_1.get_pos_x(), self.player_1.get_pos_y()] == const.PLAYER_FRONT:
                self.tiles[self.player_1.get_pos_x(), self.player_1.get_pos_y()] = const.GRASS
            self.player_1.move(x, y)
            self.tiles[x, y] = const.PLAYER_FRONT
        elif(p == 2):
            if self.tiles[self.player_2.get_pos_x(), self.player_2.get_pos_y()] == const.PLAYER_FRONT2:
                self.tiles[self.player_2.get_pos_x(), self.player_2.get_pos_y()] = const.GRASS
            self.player_2.move(x, y)
            self.tiles[x, y] = const.PLAYER_FRONT2
        elif(p == 3):
            if self.tiles[self.monster_1.get_pos_x(), self.monster_1.get_pos_y()] == const.MONSTER:
                self.tiles[self.monster_1.get_pos_x(), self.monster_1.get_pos_y()] = const.GRASS
            self.monster_1.move(x,y)
            self.tiles[x,y] = const.MONSTER
        elif (p == 4):
            if self.tiles[self.monster_2.get_pos_x(), self.monster_2.get_pos_y()] == const.MONSTER:
                self.tiles[self.monster_2.get_pos_x(), self.monster_2.get_pos_y()] = const.GRASS
            self.monster_2.move(x, y)
            self.tiles[x, y] = const.MONSTER
        elif (p == 5):
            if self.tiles[self.monster_3.get_pos_x(), self.monster_3.get_pos_y()] == const.MONSTER:
                self.tiles[self.monster_3.get_pos_x(), self.monster_3.get_pos_y()] = const.GRASS
            self.monster_3.move(x, y)
            self.tiles[x, y] = const.MONSTER

    def place_bomb(self, x, y):

        if x != 0 and y != 0:
            self.tiles[x, y] = const.BOMB

    def explode(self, x, y, player):

        for i in [x, x - 1, x - 2, x - 3, x - 4, x - 5]:
            if self.player_1.get_pos_x() == i and self.player_1.get_pos_y() == y:
                self.player_1.numOfLives -= 1

                if(self.player_1.numOfLives == 0):
                    self.player_1.isDead = True
                    self.player_1.destroy()
                else:
                    self.player_1.move(1,1)
                    self.tiles[1,1] = const.PLAYER_FRONT

            if self.player_2.get_pos_x() == i and self.player_2.get_pos_y() == y:
                self.player_2.numOfLives -= 1

                if (self.player_2.numOfLives == 0):
                    self.player_2.isDead = True
                    self.player_2.destroy()
                else:
                    self.player_2.move(17, 17)
                    self.tiles[17, 17] = const.PLAYER_FRONT2

            if self.monster_1.get_pos_x() == i and self.monster_1.get_pos_y() == y:
                self.monster_1.isDead = True
                self.tiles[self.monster_1.get_pos_x(),self.monster_1.get_pos_y()] = const.GRASS
                self.monster_1.destroy()
                if(player == 1):
                    self.player_1.points += 100
                else:
                    self.player_2.points += 100

            if self.monster_2.get_pos_x() == i and self.monster_2.get_pos_y() == y:
                self.monster_2.isDead = True
                self.tiles[self.monster_2.get_pos_x(), self.monster_2.get_pos_y()]= const.GRASS
                self.monster_2.destroy()
                if (player == 1):
                    self.player_1.points += 100
                else:
                    self.player_2.points += 100

            if self.monster_3.get_pos_x() == i and self.monster_3.get_pos_y() == y:
                self.monster_3.isDead = True
                self.tiles[self.monster_3.get_pos_x(), self.monster_3.get_pos_y()]= const.GRASS
                self.monster_3.destroy()
                if (player == 1):
                    self.player_1.points += 100
                else:
                    self.player_2.points += 100


            if self.tiles[i, y] == const.WOOD:
                self.tiles[i, y] = const.EXPLOSION
                break
            if self.tiles[i, y] != const.WALL:
                self.tiles[i, y] = const.EXPLOSION
            else:
                break

        for i in [x + 1, x + 2, x + 3, x + 4, x + 5]:
            if self.player_1.get_pos_x() == i and self.player_1.get_pos_y() == y:
                self.player_1.numOfLives -= 1
                if (self.player_1.numOfLives == 0):
                    self.player_1.isDead = True
                    self.player_1.destroy()
                else:
                    self.player_1.move(1, 1)
                    self.tiles[1, 1] = const.PLAYER_FRONT

            if self.player_2.get_pos_x() == i and self.player_2.get_pos_y() == y:
                self.player_2.numOfLives -= 1
                if (self.player_2.numOfLives == 0):
                    self.player_2.isDead = True
                    self.player_2.destroy()
                else:
                    self.player_2.move(17, 17)
                    self.tiles[17, 17] = const.PLAYER_FRONT2

            if self.monster_1.get_pos_x() == i and self.monster_1.get_pos_y() == y:
                self.monster_1.isDead = True
                self.tiles[self.monster_1.get_pos_x(),self.monster_1.get_pos_y()] = const.GRASS
                self.monster_1.destroy()
                if (player == 1):
                    self.player_1.points += 100
                else:
                    self.player_2.points += 100

            if self.monster_2.get_pos_x() == i and self.monster_2.get_pos_y() == y:
                self.monster_2.isDead = True
                self.tiles[self.monster_2.get_pos_x(), self.monster_2.get_pos_y()]= const.GRASS
                self.monster_2.destroy()
                if (player == 1):
                    self.player_1.points += 100
                else:
                    self.player_2.points += 100

            if self.monster_3.get_pos_x() == i and self.monster_3.get_pos_y() == y:
                self.monster_3.isDead = True
                self.tiles[self.monster_3.get_pos_x(), self.monster_3.get_pos_y()]= const.GRASS
                self.monster_3.destroy()
                if (player == 1):
                    self.player_1.points += 100
                else:
                    self.player_2.points += 100

            if self.tiles[i, y] == const.WOOD:
                self.tiles[i, y] = const.EXPLOSION
                break
            if self.tiles[i, y] != const.WALL:
                self.tiles[i, y] = const.EXPLOSION
            else:
                break

        for i in [y, y - 1, y - 2, y - 3, y - 4, y - 5]:
            if self.player_1.get_pos_x() == x and self.player_1.get_pos_y() == i:
                self.player_1.numOfLives -= 1
                if (self.player_1.numOfLives == 0):
                    self.player_1.isDead = True
                    self.player_1.destroy()
                else:
                    self.player_1.move(1, 1)
                    self.tiles[1, 1] = const.PLAYER_FRONT

            if self.player_2.get_pos_x() == x and self.player_2.get_pos_y() == i:
                self.player_2.numOfLives -= 1
                if (self.player_2.numOfLives == 0):
                    self.player_2.isDead = True
                    self.player_2.destroy()
                else:
                    self.player_2.move(17, 17)
                    self.tiles[17, 17] = const.PLAYER_FRONT2

            if self.monster_1.get_pos_x() == x and self.monster_1.get_pos_y() == i:
                self.monster_1.isDead = True
                self.tiles[self.monster_1.get_pos_x(),self.monster_1.get_pos_y()] = const.GRASS
                self.monster_1.destroy()
                if (player == 1):
                    self.player_1.points += 100
                else:
                    self.player_2.points += 100

            if self.monster_2.get_pos_x() == x and self.monster_2.get_pos_y() == i:
                self.monster_2.isDead = True
                self.tiles[self.monster_2.get_pos_x(), self.monster_2.get_pos_y()]= const.GRASS
                self.monster_2.destroy()
                if (player == 1):
                    self.player_1.points += 100
                else:
                    self.player_2.points += 100

            if self.monster_3.get_pos_x() == x and self.monster_3.get_pos_y() == i:
                self.monster_3.isDead = True
                self.tiles[self.monster_3.get_pos_x(), self.monster_3.get_pos_y()]= const.GRASS
                self.monster_3.destroy()
                if (player == 1):
                    self.player_1.points += 100
                else:
                    self.player_2.points += 100

            if self.tiles[x, i] == const.WOOD:
                self.tiles[x, i] = const.EXPLOSION
                break
            if self.tiles[x, i] != const.WALL:
                self.tiles[x, i] = const.EXPLOSION
            else:
                break

        for i in [y + 1, y + 2, y + 3, y + 4, y + 5]:
            if self.player_1.get_pos_x() == x and self.player_1.get_pos_y() == i:
                self.player_1.numOfLives -= 1
                if (self.player_1.numOfLives == 0):
                    self.player_1.isDead = True
                    self.player_1.destroy()
                else:
                    self.player_1.move(1, 1)
                    self.tiles[1, 1] = const.PLAYER_FRONT

            if self.player_2.get_pos_x() == x and self.player_2.get_pos_y() == i:
                self.player_2.numOfLives -= 1
                if (self.player_2.numOfLives == 0):
                    self.player_2.isDead = True
                    self.player_2.destroy()
                else:
                    self.player_2.move(17, 17)
                    self.tiles[17, 17] = const.PLAYER_FRONT2

            if self.monster_1.get_pos_x() == x and self.monster_1.get_pos_y() == i:
                self.monster_1.isDead = True
                self.tiles[self.monster_1.get_pos_x(),self.monster_1.get_pos_y()] = const.GRASS
                self.monster_1.destroy()
                if (player == 1):
                    self.player_1.points += 100
                else:
                    self.player_2.points += 100

            if self.monster_2.get_pos_x() == x and self.monster_2.get_pos_y() == i:
                self.monster_2.isDead = True
                self.tiles[self.monster_2.get_pos_x(), self.monster_2.get_pos_y()]= const.GRASS
                self.monster_2.destroy()
                if (player == 1):
                    self.player_1.points += 100
                else:
                    self.player_2.points += 100

            if self.monster_3.get_pos_x() == x and self.monster_3.get_pos_y() == i:
                self.monster_3.isDead = True
                self.tiles[self.monster_3.get_pos_x(), self.monster_3.get_pos_y()]= const.GRASS
                self.monster_3.destroy()
                if (player == 1):
                    self.player_1.points += 100
                else:
                    self.player_2.points += 100

            if self.tiles[x, i] == const.WOOD:
                self.tiles[x, i] = const.EXPLOSION
                break
            if self.tiles[x, i] != const.WALL:
                self.tiles[x, i] = const.EXPLOSION
            else:
                break

    def clear_explosion(self, x, y):

        for i in [x, x - 1, x - 2, x - 3, x - 4, x - 5]:
            if(i>0):
                if self.tiles[i, y] == const.EXPLOSION:
                    self.tiles[i, y] = const.GRASS

        for i in [x + 1, x + 2, x + 3, x + 4, x + 5]:
            if(i<19):
                if self.tiles[i, y] == const.EXPLOSION:
                    self.tiles[i, y] = const.GRASS

        for i in [y, y - 1, y - 2, y - 3, y - 4, y - 5]:
            if (i > 0):
                if self.tiles[x, i] == const.EXPLOSION:
                    self.tiles[x, i] = const.GRASS

        for i in [y + 1, y + 2, y + 3, y + 4, y + 5]:
            if (i < 19):
                if self.tiles[x, i] == const.EXPLOSION:
                    self.tiles[x, i] = const.GRASS