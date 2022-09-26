import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtQml import QQmlApplicationEngine
import os
import sys
from functools import partial
from PySide2 import QtCore, QtGui, QtQml
import Utilities as utilities
import numpy as np
import Controller
from Controller import ApolloController


# np.random.seed(102)

def main():
    QtCore.qInstallMessageHandler(utilities.qt_message_handler)
    app = QtGui.QGuiApplication(sys.argv)

    controller = ApolloController()

    engine = QtQml.QQmlApplicationEngine()
    engine.rootContext().setContextProperty("controller", controller)
    directory = os.path.dirname(os.path.abspath(__file__))
    engine.load(QtCore.QUrl.fromLocalFile(os.path.join(directory, 'views/main.qml')))
    if not engine.rootObjects():
        return -1

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())