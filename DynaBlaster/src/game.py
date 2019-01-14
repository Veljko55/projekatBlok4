import time
from PyQt5.QtWidgets import QWidget, qApp, QLabel
from PyQt5.QtCore import QTimer, Qt, QEvent, QThread, pyqtSignal
from PyQt5.QtGui import QPainter, QPixmap
import _thread

import xml.dom.minidom as xml
import numpy as np

from src import constants as const
from src import board

# noinspection PyArgumentList


class Game(QWidget):

    gameOverSignal = pyqtSignal()
    levelUpSignal = pyqtSignal()

    def __init__(self, players,lvl):


        super(Game, self).__init__()
        qApp.installEventFilter(self)
        self.released = True
        self.players = players

        self.level = lvl

        self.board = board.Board(players)
        self.timers = []
        self.timer = QTimer()
        self.timer.setInterval(const.GAME_SPEED)
        self.timer.timeout.connect(self.repaint)
        self.timer.start()

        #kretnja cudovista
        self.speed = 1/self.level
        _thread.start_new_thread(self.MoveMonster1,(self.speed,))
        _thread.start_new_thread(self.MoveMonster2, (self.speed,))
        _thread.start_new_thread(self.MoveMonster3, (self.speed,))

        #provera kolizije
        _thread.start_new_thread(self.CheckColision1,(1,))
        _thread.start_new_thread(self.ChechColision2, (1,))

        #level/gameOver thread
        _thread.start_new_thread(self.CheckGame, (1,))




        self.nr_frame = 0
        if self.players != 0:
            self.frames = []
            self.frame = np.ones((const.BOARD_WIDTH, const.BOARD_HEIGHT), dtype=int)
            self.doc = xml.Document()
            self.root = self.doc.createElement('save')
        else:
            doc = xml.parse("autosave.xml")
            self.frames = doc.getElementsByTagName("frame")


    def CheckCoordinate(self, player , monster ):
        if(player.pos_x == monster.pos_x and player.pos_y == monster.pos_y):

            return True
        else:
            return False



    def CheckGame(self, broj):
        while True:
            if(self.board.player_1.isDead and self.board.player_2.isDead):
                self.gameOverSignal.emit()
                break
            if(self.board.monster_1.isDead and self.board.monster_2.isDead and self.board.monster_3.isDead):
                self.levelUpSignal.emit()
                break
            time.sleep(1)



    def CheckColision1(self,broj):
        while True:
            if(self.CheckCoordinate(self.board.player_1, self.board.monster_1)):
                self.board.player_1.numOfLives -= 1
                if (self.board.player_1.numOfLives == 0):
                    self.board.player_1.isDead = True
                    self.board.tiles[self.board.player_1.get_pos_x(),self.board.player_1.get_pos_y()] = const.GRASS
                else:
                    self.board.monster_1.move(self.board.player_1.get_pos_x(), self.board.player_1.get_pos_y())
                    self.board.tiles[self.board.player_1.get_pos_x(), self.board.player_1.get_pos_y()] = const.MONSTER
                    self.board.player_1.move(1, 1)
                    self.board.tiles[1, 1] = const.PLAYER_FRONT

            if (self.CheckCoordinate(self.board.player_1, self.board.monster_2)):
                self.board.player_1.numOfLives -= 1
                if (self.board.player_1.numOfLives == 0):
                    self.board.player_1.isDead = True
                    self.board.tiles[self.board.player_1.get_pos_x(), self.board.player_1.get_pos_y()] = const.GRASS

                else:
                    self.board.monster_2.move(self.board.player_1.get_pos_x(), self.board.player_1.get_pos_y())
                    self.board.tiles[self.board.player_1.get_pos_x(), self.board.player_1.get_pos_y()] = const.MONSTER
                    self.board.player_1.move(1, 1)
                    self.board.tiles[1, 1] = const.PLAYER_FRONT

            if (self.CheckCoordinate(self.board.player_1, self.board.monster_3)):
                self.board.player_1.numOfLives -= 1
                if (self.board.player_1.numOfLives == 0):
                    self.board.player_1.isDead = True
                    self.board.tiles[self.board.player_1.get_pos_x(), self.board.player_1.get_pos_y()] = const.GRASS

                else:
                    self.board.monster_3.move(self.board.player_1.get_pos_x(), self.board.player_1.get_pos_y())
                    self.board.tiles[self.board.player_1.get_pos_x(), self.board.player_1.get_pos_y()] = const.MONSTER
                    self.board.player_1.move(1, 1)
                    self.board.tiles[1, 1] = const.PLAYER_FRONT

            time.sleep(0.5)

    def ChechColision2(self, broj):
        while True:
            if(self.CheckCoordinate(self.board.player_2, self.board.monster_1)):
                self.board.player_2.numOfLives -= 1
                if (self.board.player_2.numOfLives == 0):
                    self.board.player_2.isDead = True
                    self.board.tiles[self.board.player_2.get_pos_x(), self.board.player_2.get_pos_y()] = const.GRASS
                else:
                    self.board.monster_1.move(self.board.player_2.get_pos_x(), self.board.player_2.get_pos_y())
                    self.board.tiles[self.board.player_2.get_pos_x(), self.board.player_2.get_pos_y()] = const.MONSTER
                    self.board.player_2.move(17, 17)
                    self.board.tiles[17, 17] = const.PLAYER_FRONT2

            if (self.CheckCoordinate(self.board.player_2, self.board.monster_2)):
                self.board.player_2.numOfLives -= 1
                if (self.board.player_2.numOfLives == 0):
                    self.board.player_2.isDead = True
                    self.board.tiles[self.board.player_2.get_pos_x(), self.board.player_2.get_pos_y()] = const.GRASS

                else:
                    self.board.monster_2.move(self.board.player_2.get_pos_x(), self.board.player_2.get_pos_y())
                    self.board.tiles[self.board.player_2.get_pos_x(), self.board.player_2.get_pos_y()] = const.MONSTER
                    self.board.player_2.move(17, 17)
                    self.board.tiles[self.board.player_2.get_pos_x(), self.board.player_2.get_pos_y()] = const.PLAYER_FRONT2

            if (self.CheckCoordinate(self.board.player_2, self.board.monster_3)):
                self.board.player_2.numOfLives -= 1
                if (self.board.player_2.numOfLives == 0):
                    self.board.player_2.isDead = True
                    self.board.tiles[self.board.player_2.get_pos_x(), self.board.player_2.get_pos_y()] = const.GRASS

                else:
                    self.board.monster_3.move(self.board.player_2.get_pos_x(), self.board.player_2.get_pos_y())
                    self.board.tiles[self.board.player_2.get_pos_x(), self.board.player_2.get_pos_y()] = const.MONSTER
                    self.board.player_2.move(17, 17)
                    self.board.tiles[17, 17] = const.PLAYER_FRONT2

            time.sleep(0.5)


    def MoveMonster1(self, movementSpeed):

        while not self.board.monster_1.isDead:
            while not self.board.monster_1.isDead :
                m1Y = self.board.monster_1.get_pos_y()
                m1X = self.board.monster_1.get_pos_x()

                if(self.board.try_moveM(m1X, m1Y + 1)):
                    self.board.move(m1X , m1Y + 1, 3)
                else:
                    break

                print(1)
                time.sleep(movementSpeed)

            while not self.board.monster_1.isDead :
                m1Y = self.board.monster_1.get_pos_y()
                m1X = self.board.monster_1.get_pos_x()

                if(self.board.try_moveM(m1X, m1Y - 1)):
                    self.board.move(m1X , m1Y - 1, 3)
                else:
                    break


                print(1)
                time.sleep(movementSpeed)

            while  not self.board.monster_1.isDead :
                m1Y = self.board.monster_1.get_pos_y()
                m1X = self.board.monster_1.get_pos_x()

                if(self.board.try_moveM(m1X + 1, m1Y)):
                    self.board.move(m1X + 1 , m1Y, 3)
                else:
                    break


                print(1)
                time.sleep(movementSpeed)

            while  not self.board.monster_1.isDead :
                m1Y = self.board.monster_1.get_pos_y()
                m1X = self.board.monster_1.get_pos_x()

                if(self.board.try_moveM(m1X - 1, m1Y)):
                    self.board.move(m1X - 1 , m1Y, 3)
                else:
                    break


                print(1)
                time.sleep(movementSpeed)

    def MoveMonster2(self, movementSpeed):

        while not self.board.monster_2.isDead:
            while not self.board.monster_2.isDead :
                m1Y = self.board.monster_2.get_pos_y()
                m1X = self.board.monster_2.get_pos_x()

                if(self.board.try_moveM(m1X, m1Y + 1)):
                    self.board.move(m1X , m1Y + 1, 4)
                else:
                    break

                print(1)
                time.sleep(movementSpeed)

            while not self.board.monster_2.isDead :
                m1Y = self.board.monster_2.get_pos_y()
                m1X = self.board.monster_2.get_pos_x()

                if(self.board.try_moveM(m1X, m1Y - 1)):
                    self.board.move(m1X , m1Y - 1, 4)
                else:
                    break


                print(1)
                time.sleep(movementSpeed)

            while  not self.board.monster_2.isDead :
                m1Y = self.board.monster_2.get_pos_y()
                m1X = self.board.monster_2.get_pos_x()

                if(self.board.try_moveM(m1X + 1, m1Y)):
                    self.board.move(m1X + 1 , m1Y, 4)
                else:
                    break


                print(1)
                time.sleep(movementSpeed)

            while  not self.board.monster_2.isDead :
                m1Y = self.board.monster_2.get_pos_y()
                m1X = self.board.monster_2.get_pos_x()

                if(self.board.try_moveM(m1X - 1, m1Y)):
                    self.board.move(m1X - 1 , m1Y, 4)
                else:
                    break


                print(1)
                time.sleep(movementSpeed)

    def MoveMonster3(self, movementSpeed):

        while not self.board.monster_3.isDead:
            while not self.board.monster_3.isDead :
                m1Y = self.board.monster_3.get_pos_y()
                m1X = self.board.monster_3.get_pos_x()

                if(self.board.try_moveM(m1X, m1Y + 1)):
                    self.board.move(m1X , m1Y + 1, 5)
                else:
                    break

                print(1)
                time.sleep(movementSpeed)

            while not self.board.monster_3.isDead :
                m1Y = self.board.monster_3.get_pos_y()
                m1X = self.board.monster_3.get_pos_x()

                if(self.board.try_moveM(m1X, m1Y - 1)):
                    self.board.move(m1X , m1Y - 1, 5)
                else:
                    break


                print(1)
                time.sleep(movementSpeed)

            while  not self.board.monster_3.isDead :
                m1Y = self.board.monster_3.get_pos_y()
                m1X = self.board.monster_3.get_pos_x()

                if(self.board.try_moveM(m1X + 1, m1Y)):
                    self.board.move(m1X + 1 , m1Y, 5)
                else:
                    break


                print(1)
                time.sleep(movementSpeed)

            while  not self.board.monster_3.isDead :
                m1Y = self.board.monster_3.get_pos_y()
                m1X = self.board.monster_3.get_pos_x()

                if(self.board.try_moveM(m1X - 1, m1Y)):
                    self.board.move(m1X - 1 , m1Y, 5)
                else:
                    break


                print(1)
                time.sleep(movementSpeed)

    def paintEvent(self, event):

        painter = QPainter()
        painter.begin(self)
        self.draw_board(painter)
        painter.end()

    def draw_board(self, painter):

        width = const.TILE_WIDTH
        height = const.TILE_HEIGHT

        self.nr_frame += 1
        if self.players == 0:
            self.get_from_xml()

        for x in range(const.BOARD_WIDTH):
            for y in range(const.BOARD_HEIGHT):
                pos_x = x * width
                pos_y = y * height

                if self.board.tiles[x, y] == const.WALL:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/wall.png'))
                elif self.board.tiles[x, y] == const.GRASS:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/grass.png'))
                elif self.board.tiles[x, y] == const.WOOD:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/wood.png'))
                elif self.board.tiles[x, y] == const.PLAYER_FRONT:
                    if self.board.player_1.isDead:
                        painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/grass.png'))
                    else:
                        painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/player_front.png'))
                elif self.board.tiles[x, y] == const.PLAYER_FRONT2:
                    if self.board.player_2.isDead:
                        painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/grass.png'))
                    else:
                        painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/player_front2.png'))
                elif self.board.tiles[x, y] == const.BOMB:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/bomb.png'))
                elif self.board.tiles[x, y] == const.EXPLOSION:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/explosion.png'))
                elif self.board.tiles[x, y] == const.MONSTER:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/monster.png'))
                else:
                    painter.drawPixmap(pos_x, pos_y, width, height, QPixmap('../res/images/wall.png'))

        if self.players != 0:
            self.check_changes()

    def eventFilter(self, obj, event):

        if event.type() == QEvent.KeyRelease:
            self.released = True

        if event.type() == QEvent.KeyPress and self.released and self.players != 0:
            self.released = False
            if not self.board.player_1.isDead:
                x = self.board.player_1.get_pos_x()
                y = self.board.player_1.get_pos_y()

                if event.key() == Qt.Key_W:
                    if self.board.try_move(x, y - 1):
                        self.board.move(x, y - 1,1)
                elif event.key() == Qt.Key_S:
                    if self.board.try_move(x, y + 1):
                        self.board.move(x, y + 1,1)
                elif event.key() == Qt.Key_A:
                    if self.board.try_move(x - 1, y):
                        self.board.move(x - 1, y,1)
                elif event.key() == Qt.Key_D:
                    if self.board.try_move(x + 1, y):
                        self.board.move(x + 1, y,1)
                elif event.key() == Qt.Key_F:
                    x, y = self.board.player_1.place_bomb()
                    if x != 0 and y != 0:
                        self.board.place_bomb(x, y)
                        self.timers.append(QTimer())
                        self.timers[len(self.timers) - 1].setInterval(const.BOMB_SPEED/self.level)
                        timer = self.timers[len(self.timers) - 1]
                        timer.timeout.connect(lambda :self.explode(x, y,1))
                        timer.timeout.connect(timer.stop)
                        timer.start()

            if not self.board.player_2.isDead:
                x1 = self.board.player_2.get_pos_x()
                y1= self.board.player_2.get_pos_y()

                if event.key() == Qt.Key_Up:
                    if self.board.try_move(x1, y1 - 1):
                        self.board.move(x1, y1 - 1,2)
                elif event.key() == Qt.Key_Down:
                    if self.board.try_move(x1, y1 + 1):
                        self.board.move(x1, y1 + 1,2)
                elif event.key() == Qt.Key_Left:
                    if self.board.try_move(x1 - 1, y1):
                        self.board.move(x1 - 1, y1,2)
                elif event.key() == Qt.Key_Right:
                    if self.board.try_move(x1 + 1, y1):
                        self.board.move(x1 + 1, y1,2)
                elif event.key() == Qt.Key_Enter:
                    x1, y1 = self.board.player_2.place_bomb()
                    if x1 != 0 and y1 != 0:
                        self.board.place_bomb(x1, y1)
                        self.timers.append(QTimer())
                        self.timers[len(self.timers) - 1].setInterval(const.BOMB_SPEED/self.level)
                        timer = self.timers[len(self.timers) - 1]
                        timer.timeout.connect(lambda :self.explode(x1, y1, 2))
                        timer.timeout.connect(timer.stop)
                        timer.start()

        return super(Game, self).eventFilter(obj, event)

    def explode(self, x, y, p):


        self.board.explode(x, y, p)

        if(p == 1):
            self.board.player_1.give_bomb()
            self.timers.append(QTimer())
            self.timers[len(self.timers) - 1].setInterval(const.EXPLOSION_SPEED)
            timer = self.timers[len(self.timers) - 1]
            timer.timeout.connect(lambda: self.board.clear_explosion(x, y))
            timer.timeout.connect(timer.stop)
            timer.start()

        else:
            self.board.player_2.give_bomb()
            self.timers.append(QTimer())
            self.timers[len(self.timers) - 1].setInterval(const.EXPLOSION_SPEED)
            timer = self.timers[len(self.timers) - 1]
            timer.timeout.connect(lambda: self.board.clear_explosion(x, y))
            timer.timeout.connect(timer.stop)
            timer.start()

    def check_changes(self):

        if not np.array_equal(self.frame, self.board.tiles):
            self.board.save_change(self.frame)
            self.frame = np.copy(self.board.tiles)
            self.frames.append(self.nr_frame)