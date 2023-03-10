from PyQt5 import QtCore, QtGui, QtWidgets
import os
import sys
import subprocess


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)

        self.hiddenEnabled = False

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.treeview = QtWidgets.QTreeView(self.centralwidget)
        self.treeview.setMaximumSize(QtCore.QSize(250, 16777215))
        self.treeview.setObjectName("treeview")
        self.horizontalLayout.addWidget(self.treeview)

        self.listview = QtWidgets.QTreeView(self.centralwidget)
        self.listview.setObjectName("listview")
        self.horizontalLayout.addWidget(self.listview)

        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        path = "QtCore.QDir.rootPath()"
        self.copyPath = ""
        self.copyList = []
        self.copyListNew = ""

        self.dirModel = QtWidgets.QFileSystemModel()
        self.dirModel.setReadOnly(False)

        self.dirModel.setRootPath(path)

        self.fileModel = QtWidgets.QFileSystemModel()
        self.fileModel.setReadOnly(False)
        # self.fileModel.setResolveSymlinks(True)
        self.fileModel.setRootPath(path)

        self.treeview.setModel(self.dirModel)
        self.treeview.hideColumn(1)
        self.treeview.hideColumn(2)
        self.treeview.hideColumn(3)
        self.treeview.setRootIsDecorated(True)

        self.treeview.setTreePosition(0)
        self.treeview.setUniformRowHeights(True)
        self.treeview.setExpandsOnDoubleClick(True)
        self.treeview.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeview.setIndentation(12)
        self.treeview.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.treeview.setDragEnabled(True)
        self.treeview.setAcceptDrops(True)
        self.treeview.setDropIndicatorShown(True)

        self.treeview.selectionModel().selectionChanged.connect(self.on_selectionChanged)

        self.listview.setModel(self.fileModel)
        self.listview.doubleClicked.connect(self.list_doubleClicked)

        self.listview.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listview.setDragEnabled(True)
        self.listview.setAcceptDrops(True)
        self.listview.setDropIndicatorShown(True)
        self.listview.sortByColumn(0, QtCore.Qt.AscendingOrder)

        # Переопределение размера для колонок листа #

        self.listview.header().resizeSection(0, 250)
        self.listview.header().resizeSection(1, 80)
        self.listview.header().resizeSection(2, 80)

        ##########################################

        # Включение сортировки для колонок #

        self.listview.setSortingEnabled(True)
        self.treeview.setSortingEnabled(True)

        ##########################################

        self.listview.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeview.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        self.listview.setIndentation(10)
        self.getRowCount()

    def getRowCount(self):
        count = 0
        index = self.treeview.selectionModel().currentIndex()
        path = QtCore.QDir(self.dirModel.fileInfo(index).absoluteFilePath())
        count = len(path.entryList(QtCore.QDir.Files))

        if index == QtCore.QDir.rootPath():
            count = 0

        self.statusbar.showMessage("%s %s" %
                                   (count, "Files"), 0)
        return count

    def on_selectionChanged(self):
        # self.treeview.selectionModel().clearSelection()
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.listview.setRootIndex(self.fileModel.setRootPath(path))
        self.currentPath = path
        self.getRowCount()

    def list_doubleClicked(self):
        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).absoluteFilePath()
        if not self.fileModel.fileInfo(index).isDir():
            os.startfile(str(path))
        # else:
        #     self.treeview.setCurrentIndex(self.dirModel.index(path))
        #     self.treeview.setFocus()


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    MainWindow.setWindowTitle("FileManager")
    sys.exit(app.exec_())
