from PySide2.QtCore import *
from PySide2 import QtCore, QtGui, QtQml


class ApolloView(QtCore.QAbstractListModel):
    TextRole = QtCore.Qt.UserRole + 1000
    AgentRole = QtCore.Qt.UserRole + 1001

    def __init__(self, parent=None):
        super(ApolloView, self).__init__(parent)
        self._entries = []

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid(): return 0
        return len(self._entries)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if 0 <= index.row() < self.rowCount() and index.isValid():
            item = self._entries[index.row()]
            if role == ApolloView.TextRole:
                return item["message"]
            elif role == ApolloView.AgentRole:
                return item["agent"]

    def roleNames(self):
        roles = dict()
        roles[ApolloView.TextRole] = b"message"
        roles[ApolloView.AgentRole] = b"agent"
        return roles

    def insertRows(self, n, t):
        # self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self.beginInsertRows(QtCore.QModelIndex(), 0, 0)
        # self._entries.append(dict(message=n, agent=t))

        self._entries.insert(0,dict(message=n, agent=t))
        self.endInsertRows()
        return True