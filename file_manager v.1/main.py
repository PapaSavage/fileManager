from PyQt5 import QtCore, QtGui, QtWidgets


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

        path = QtCore.QDir.rootPath()
        self.copyPath = ""
        self.copyList = []
        self.copyListNew = ""

        self.dirModel = QtWidgets.QFileSystemModel()
        self.dirModel.setReadOnly(False)
        self.dirModel.setFilter(QtCore.QDir.NoDotAndDotDot |
                                QtCore.QDir.AllDirs | QtCore.QDir.Drives)
        self.dirModel.setRootPath(QtCore.QDir.rootPath())

        self.fileModel = QtWidgets.QFileSystemModel()
        self.fileModel.setReadOnly(False)
        self.fileModel.setFilter(QtCore.QDir.NoDotAndDotDot |
                                 QtCore.QDir.AllDirs | QtCore.QDir.Files)
        # self.fileModel.setResolveSymlinks(True)
        self.fileModel.setRootPath(QtCore.QDir.rootPath())

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
        # self.treeview.sortByColumn(0, QtWidgets.Qt.AscendingOrder)

        self.treeview.selectionModel().selectionChanged.connect(self.on_selectionChanged)

        self.listview.setModel(self.fileModel)
        self.listview.doubleClicked.connect(self.list_doubleClicked)

        self.listview.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.listview.setDragEnabled(True)
        self.listview.setAcceptDrops(True)
        self.listview.setDropIndicatorShown(True)

        self.listview.header().resizeSection(0, 250)
        self.listview.header().resizeSection(1, 80)
        self.listview.header().resizeSection(2, 80)
        self.listview.setSortingEnabled(True)
        self.treeview.setSortingEnabled(True)

        # Открытие папки по дабл-клику #

        self.listview.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.treeview.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)

        ##########################################

        self.listview.setIndentation(10)
        # self.listview.sortByColumn(0, Qt.AscendingOrder)
        self.enableHidden()
        self.getRowCount()

    def enableHidden(self):
        if self.hiddenEnabled == False:
            self.fileModel.setFilter(
                QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Hidden | QtCore.QDir.AllDirs | QtCore.QDir.Files)
            self.dirModel.setFilter(
                QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Hidden | QtCore.QDir.AllDirs)
            self.hiddenEnabled = True
            # self.hiddenAction.setChecked(True)
            print("set hidden files to true")

    def getRowCount(self):
        count = 0
        index = self.treeview.selectionModel().currentIndex()
        path = QtCore.QDir(self.dirModel.fileInfo(index).absoluteFilePath())
        count = len(path.entryList(QtCore.QDir.Files))
        # self.statusBar().showMessage("%s %s" % (count, "Files"), 0)
        return count

    def on_selectionChanged(self):
        self.treeview.selectionModel().clearSelection()
        index = self.treeview.selectionModel().currentIndex()
        path = self.dirModel.fileInfo(index).absoluteFilePath()
        self.listview.setRootIndex(self.fileModel.setRootPath(path))
        self.currentPath = path
        self.getRowCount()

    def list_doubleClicked(self):
        index = self.listview.selectionModel().currentIndex()
        path = self.fileModel.fileInfo(index).absoluteFilePath()
#        folderpath = self.fileModel.fileInfo(index).path()
        if not self.fileModel.fileInfo(index).isDir():
            if self.checkIsApplication(path) == True:
                self.process.startDetached(path)
            else:
                QtWidgets.QDesktopServices.openUrl(
                    QtWidgets.QUrl(path, QtWidgets.QUrl.TolerantMode | QtWidgets.QUrl.EncodeUnicode))
        else:
            self.treeview.setCurrentIndex(self.dirModel.index(path))
            self.treeview.setFocus()
#            self.listview.setRootIndex(self.fileModel.setRootPath(path))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    MainWindow.setWindowTitle("FileManager")
    # if len(sys.argv) > 1:
    #     path = QtCore.QDir.rootPath()
    #     print(path)
    #     MainWindow.listview.setRootIndex(
    #         MainWindow.fileModel.setRootPath(path))
    sys.exit(app.exec_())
