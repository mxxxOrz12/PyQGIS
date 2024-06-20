# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(936, 600)
        MainWindow.setBaseSize(QtCore.QSize(1000, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/qgis.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 936, 22))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        self.ConnectDataBase = QtWidgets.QMenu(self.menubar)
        self.ConnectDataBase.setObjectName("ConnectDataBase")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.dockWidget_3 = QtWidgets.QDockWidget(MainWindow)
        self.dockWidget_3.setMaximumSize(QtCore.QSize(300, 1000))
        self.dockWidget_3.setObjectName("dockWidget_3")
        self.dockWidgetContents_1 = QtWidgets.QWidget()
        self.dockWidgetContents_1.setObjectName("dockWidgetContents_1")
        self.dockWidget_3.setWidget(self.dockWidgetContents_1)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_3)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionOpenRaster = QtWidgets.QAction(MainWindow)
        self.actionOpenRaster.setObjectName("actionOpenRaster")
        self.actionOpenVector = QtWidgets.QAction(MainWindow)
        self.actionOpenVector.setObjectName("actionOpenVector")
        self.actionArea = QtWidgets.QAction(MainWindow)
        self.actionArea.setObjectName("actionArea")
        self.actionDistance = QtWidgets.QAction(MainWindow)
        self.actionDistance.setObjectName("actionDistance")
        self.actionConnect = QtWidgets.QAction(MainWindow)
        self.actionConnect.setObjectName("actionConnect")
        self.actionCloseConnect = QtWidgets.QAction(MainWindow)
        self.actionCloseConnect.setObjectName("actionCloseConnect")
        self.menu.addSeparator()
        self.menu.addAction(self.actionOpenVector)
        self.menu.addAction(self.actionOpenRaster)
        self.menu_3.addAction(self.actionArea)
        self.menu_3.addAction(self.actionDistance)
        self.ConnectDataBase.addAction(self.actionConnect)
        self.ConnectDataBase.addAction(self.actionCloseConnect)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.ConnectDataBase.menuAction())
        self.toolBar.addAction(self.actionOpenVector)
        self.toolBar.addAction(self.actionOpenRaster)
        self.toolBar.addAction(self.actionArea)
        self.toolBar.addAction(self.actionDistance)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GIS桌面软件-马骁"))
        self.menu.setTitle(_translate("MainWindow", "打开"))
        self.menu_2.setTitle(_translate("MainWindow", "搜索"))
        self.menu_3.setTitle(_translate("MainWindow", "测量"))
        self.ConnectDataBase.setTitle(_translate("MainWindow", "连接数据库"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionOpenRaster.setText(_translate("MainWindow", "打开栅格"))
        self.actionOpenVector.setText(_translate("MainWindow", "打开矢量"))
        self.actionArea.setText(_translate("MainWindow", "面积量算"))
        self.actionDistance.setText(_translate("MainWindow", "距离量算"))
        self.actionConnect.setText(_translate("MainWindow", "连接"))
        self.actionCloseConnect.setText(_translate("MainWindow", "关闭"))
import myRc_rc
