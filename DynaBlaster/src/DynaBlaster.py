import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QApplication
from multiprocessing import Process, Queue
from src import gui

# PyQt Debugging
# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

def Muzika():
    muzika = QMediaPlayer()
    muzika.setMedia(QMediaContent(QUrl('C:/Users/Racunar/Desktop/najazurnija2DynaBlaster\res\sound')))
    muzika.play()


class QMediaContetn(object):
    pass


if __name__ == '__main__':

    app = QApplication(sys.argv)
    game = gui.Window()

    # sys.exit(app.exec_())
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
