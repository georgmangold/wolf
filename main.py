import sys

from PySide6 import QtGui, QtWidgets

from controller import Controller

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pixmap = QtGui.QPixmap("gfx/wolf_logo.jpeg")
    pixmap = pixmap.scaled(640, 480)
    splash = QtWidgets.QSplashScreen(pixmap)
    splash.show()
    controller = Controller()
    controller.show_main_window()
    splash.finish(controller.ui)
    app.exec()
