import sys

from PySide6 import QtGui, QtWidgets
from PySide6.QtCore import Qt, QTimer
from time import sleep
from qt_material import apply_stylesheet

from controller import Controller

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_stylesheet(app, theme='light_teal.xml')
    pixmap = QtGui.QPixmap("gfx/wolf_splashscreen.png")
    pixmap = pixmap.scaled(640, 480)
    splash = QtWidgets.QSplashScreen(pixmap)
    splash.show()
    splash.showMessage("Lade.  ", Qt.AlignBottom | Qt.AlignHCenter)
    sleep(0.5)
    splash.showMessage("Lade.. ", Qt.AlignBottom | Qt.AlignHCenter)
    sleep(0.5)
    splash.showMessage("Lade...", Qt.AlignBottom | Qt.AlignHCenter)
    sleep(0.5)
    splash.showMessage("Lade.  ", Qt.AlignBottom | Qt.AlignHCenter)
    sleep(0.5)
    splash.showMessage("Lade.. ", Qt.AlignBottom | Qt.AlignHCenter)
    sleep(0.5)
    splash.showMessage("Lade...", Qt.AlignBottom | Qt.AlignHCenter)
    sleep(0.5)
    splash.showMessage("Noch einen schönen Tag!", Qt.AlignBottom | Qt.AlignHCenter)
    sleep(1)
    controller = Controller()
    controller.show_main_window()
    splash.finish(controller.ui)
    app.exec()
