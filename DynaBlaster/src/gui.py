import time

from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QStackedWidget, QWidget, QPushButton, QStatusBar, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QThread, QUrl
import _thread
from multiprocessing import Process

from src import game
from src import constants as const

import sys

def Music():
    print(111111)
    muzika = QMediaPlayer()
    muzika.media = QMediaContent(QUrl('../res/sound/GameMusic.mp3'))
    muzika.setMedia(QMediaContent(QUrl('../res/sound/GameMusic.mp3')))
    muzika.customAudioRole()
    muzika.setVolume(1000)

    muzika.play()

class Window(QMainWindow):

    level = 1
    player1Score = 0
    player2Score = 0
    player1lives = 3
    player2lives = 3
    player1alive = True
    player2alive = True

    def __init__(self):

        super().__init__()

        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainMenuWidget = MainMenu()
        self.game = game.Game(1,self.level)

        self.test = QStatusBar()
        self.test.setWindowTitle('Score')
        self.test.setFixedHeight(20)
        self.test.setFixedWidth(300)
        self.test.move(10, 10)
        self.test.show()

        self.menu()
        self.checkGame()

        #muzika u pozadini preko procesa
        self.procesMuzika = Process(target=self.Music(),args=())
        self.procesMuzika.start()

        ######
        self.setWindowTitle('DynaBlaster')

        self.test.showMessage('Level ' + self.level.__str__() + '\t\t\t\t\t' + ' Player1( ' + self.game.board.player_1.numOfLives.__str__() + ' ): ' + self.game.board.player_1.points.__str__() + '\t\t\t\t\t' + ' Player2( ' + self.game.board.player_2.numOfLives.__str__() + ' ): ' + self.game.board.player_2.points.__str__(), 2000)
        self.setWindowIcon(QIcon('../res/images/icon.png'))

        _thread.start_new_thread(self.pointsThread, (1,))

        self.show()

    def Music(self):
        self.muzika = QMediaPlayer()
        self.muzika.media = QMediaContent(QUrl('../res/sound/GameMusic.mp3'))
        self.muzika.setMedia(QMediaContent(QUrl('../res/sound/GameMusic.mp3')))
        self.muzika.play()

    def pointsThread(self,broj):
        while True:
            self.test.showMessage('Level ' + self.level.__str__() + '\t\t\t\t\t' + ' Player1( ' + self.game.board.player_1.numOfLives.__str__() + ' ): ' + self.game.board.player_1.points.__str__() + '\t\t\t\t\t' + ' Player2( ' + self.game.board.player_2.numOfLives.__str__() + ' ): ' + self.game.board.player_2.points.__str__(), 2000)
            time.sleep(2)

    def checkGame(self):
        self.game.levelUpSignal.connect(self.nextLevel)
        self.game.gameOverSignal.connect(self.gameOver)

    def nextLevel(self):
        self.level += 1
        self.player1Score = self.game.board.player_1.points
        self.player2Score = self.game.board.player_2.points
        self.player1lives = self.game.board.player_1.numOfLives
        self.player2lives = self.game.board.player_2.numOfLives
        self.player1alive = self.game.board.player_1.isDead
        self.player2alive = self.game.board.player_2.isDead

        self.game = game.Game(1, self.level)
        self.game.board.player_1.points = self.player1Score
        self.game.board.player_2.points = self.player2Score
        self.game.board.player_1.numOfLives = self.player1lives
        self.game.board.player_2.numOfLives = self.player2lives
        self.game.board.player_1.isDead = self.player1alive
        self.game.board.player_2.isDead = self.player2alive

        self.setCentralWidget(self.game)
        self.resize(const.BOARD_WIDTH * const.TILE_WIDTH, const.BOARD_HEIGHT * const.TILE_HEIGHT)
        self.center()
        self.test.showMessage('Level ' + self.level.__str__() + '\t\t\t\t\t' + ' Player1( ' + self.game.board.player_1.numOfLives.__str__() + ' ): ' + self.game.board.player_1.points.__str__() + '\t\t\t\t\t' + ' Player2( ' + self.game.board.player_2.numOfLives.__str__() + ' ): ' + self.game.board.player_2.points.__str__())

        self.checkGame()

    def gameOver(self):
        self.__init__()
        self.mainMenuWidget.play_button.setText('GAME OVER')
        self.mainMenuWidget.play_button.setEnabled(False)

    def center(self):

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def menu(self):

        self.mainMenuWidget.playGameSignal.connect(self.play)
        self.mainMenuWidget.quitGameSignal.connect(self.quit)

        self.centralWidget.addWidget(self.mainMenuWidget)
        self.centralWidget.setCurrentWidget(self.mainMenuWidget)

        self.resize(240, 180)
        self.center()

    def play(self):

        self.setCentralWidget(self.game)
        self.resize(const.BOARD_WIDTH * const.TILE_WIDTH, const.BOARD_HEIGHT * const.TILE_HEIGHT + 20)
        self.center()


    @staticmethod
    def quit():
        sys.exit()


class MainMenu(QWidget):

    playGameSignal = pyqtSignal()
    quitGameSignal = pyqtSignal()

    def __init__(self):
        super(MainMenu, self).__init__()

        button_width = 190
        button_height = 50
        button_offset = 25

        self.play_button = QPushButton('Play', self)
        self.play_button.setFixedWidth(button_width)
        self.play_button.setFixedHeight(button_height)
        self.play_button.move(button_offset, (button_offset * 1) + (button_height * 0))
        self.play_button.clicked.connect(self.play)

        quit_button = QPushButton('Exit', self)
        quit_button.setFixedWidth(button_width)
        quit_button.setFixedHeight(button_height)
        quit_button.move(button_offset, (button_offset * 2) + (button_height * 1))
        quit_button.clicked.connect(self.quit)

        self.show()

    def play(self):

        self.playGameSignal.emit()

    def quit(self):

        self.quitGameSignal.emit()
