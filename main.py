from qgis.PyQt import QtCore
from qgis.core import QgsApplication
from PyQt5.QtCore import Qt
import os
import traceback
from mainWindow import MainWindow

if __name__ == '__main__':
    QgsApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QgsApplication([], True)

    t = QtCore.QTranslator()
    t.load(r"./zh-Hans.qm")
    app.installTranslator(t)

    app.initQgis()

    mainWindow = MainWindow()
    mainWindow.show()
    # shp = r"D:\CUMT\GIS课程\专业课\智慧能源概论\ppt\新疆.shp"
    # tif = r"D:\CUMT\GIS课程\专业课\智慧能源概论\ppt\Ch4.tif"
    # # mainWindow.addVectorLayer(shp)
    # mainWindow.addRasterLayer(tif)

    app.exec_()
    app.exitQgis()