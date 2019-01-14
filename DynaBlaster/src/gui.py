import time
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QStackedWidget, QWidget, QPushButton, QStatusBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QThread
import _thread
import ctypes

from src import constants as const

import sys

class Window(QMainWindow):

    level = 1
    player1Score = 0
    player2Score = 0
    player1lives = 3
    player2lives = 3

    def __init__(self):

        super().__init__()

        self.centralWidget = QStackedWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainMenuWidget = MainMenu()

        self.menu()

        self.setWindowTitle('DynaBlaster')
        self.setWindowIcon(QIcon('../res/images/icon.png'))


        self.show()



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