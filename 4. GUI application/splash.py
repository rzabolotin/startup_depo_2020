from PyQt5 import QtCore, QtGui, QtWidgets


class Splash:
    def __init__(self):
        px = QtGui.QPixmap(400, 50)
        px.fill(QtCore.Qt.gray)
        px.rect()
        self.splash = QtWidgets.QSplashScreen(px)
        font = QtGui.QFont(self.splash.font())
        font.setPointSize(font.pointSize() + 5)
        self.splash.setFont(font)
        self.message = ""
        self.procent = None

    def set_message(self, text):
        self.message = text
        self.procent = None
        self.__show_message(is_start_cycle=True)

    def set_procent(self, procent):
        try:
            self.procent = int(procent)
            if self.procent < 0:
                self.procent = 0
            if self.procent > 100:
                self.procent = 100
            self.__show_message(is_start_cycle=False)
        except ValueError:
            import logging

            logging.error("Splash.set_procent. Процентное значение - не целое число")

    def __show_message(self, is_start_cycle):
        if self.message == "":
            return
        if self.procent is None:
            text = "%s..." % self.message
        else:
            text = "%s... %d%%" % (self.message, self.procent)
        self.splash.showMessage(
            text, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignCenter, QtCore.Qt.black
        )
        if True:  # is_start_cycle:
            self.splash.show()
            QtWidgets.qApp.processEvents()

    def close_message(self, parentWindow):
        self.splash.finish(parentWindow)
        self.message = ""
        self.procent = None
