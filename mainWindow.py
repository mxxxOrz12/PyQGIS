import sys
import traceback
from qgis.core import QgsProject, QgsLayerTreeModel, QgsCoordinateReferenceSystem, QgsMapSettings
from qgis.gui import QgsLayerTreeView, QgsMapCanvas, QgsLayerTreeMapCanvasBridge
from PyQt5.QtCore import QUrl, QSize, QMimeData, QUrl
from ui.ui import Ui_MainWindow
from ui.Dialog import Ui_Dialog
from PyQt5.QtWidgets import QMainWindow, QDialog,QVBoxLayout, QHBoxLayout, QFileDialog, QMessageBox, QStatusBar, QLabel, \
    QComboBox
from qgisUtils import addMapLayer, readVectorFile, readRasterFile, menuProvider
from PyQt5 import QtWidgets
PROJECT = QgsProject.instance()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # 1 修改标题
        self.setWindowTitle("PyQGIS桌面软件 -马骁")
        # 2 初始化图层树
        vl = QVBoxLayout(self.dockWidgetContents_1)
        self.layerTreeView = QgsLayerTreeView(self)
        vl.addWidget(self.layerTreeView)
        # 3 初始化地图画布
        self.mapCanvas: QgsMapCanvas = QgsMapCanvas(self)
        self.hl = QHBoxLayout(self.frame)
        self.hl.setContentsMargins(0, 0, 0, 0)  # 设置周围间距
        self.hl.addWidget(self.mapCanvas)
        # 4 设置图层树风格
        self.model = QgsLayerTreeModel(PROJECT.layerTreeRoot(), self)
        self.model.setFlag(QgsLayerTreeModel.AllowNodeRename)  # 允许图层节点重命名
        self.model.setFlag(QgsLayerTreeModel.AllowNodeReorder)  # 允许图层拖拽排序
        self.model.setFlag(QgsLayerTreeModel.AllowNodeChangeVisibility)  # 允许改变图层节点可视性
        self.model.setFlag(QgsLayerTreeModel.ShowLegendAsTree)  # 展示图例
        self.model.setAutoCollapseLegendNodes(10)  # 当节点数大于等于10时自动折叠
        self.layerTreeView.setModel(self.model)
        # 4 建立图层树与地图画布的桥接
        self.layerTreeBridge = QgsLayerTreeMapCanvasBridge(PROJECT.layerTreeRoot(), self.mapCanvas, self)
        # 5 初始加载影像
        self.firstAdd = True
        # 6 允许拖拽文件
        self.setAcceptDrops(True)

        # 7 图层树右键菜单创建
        self.rightMenuProv = menuProvider(self)
        self.layerTreeView.setMenuProvider(self.rightMenuProv)

        # 8.0 提前给予基本CRS
        self.mapCanvas.setDestinationCrs(QgsCoordinateReferenceSystem("EPSG:4326"))

        # 8 状态栏控件
        self.statusBar = QStatusBar()
        self.statusBar.setStyleSheet('color: black; border: none')
        self.statusXY = QLabel('{:<40}'.format(''))  # x y 坐标状态
        self.statusBar.addWidget(self.statusXY, 1)

        self.statusScaleLabel = QLabel('比例尺')
        self.statusScaleComboBox = QComboBox(self)
        self.statusScaleComboBox.setFixedWidth(120)
        self.statusScaleComboBox.addItems(
            ["1:500", "1:1000", "1:2500", "1:5000", "1:10000", "1:25000", "1:100000", "1:500000", "1:1000000"])
        self.statusScaleComboBox.setEditable(True)
        self.statusBar.addWidget(self.statusScaleLabel)
        self.statusBar.addWidget(self.statusScaleComboBox)

        self.statusCrsLabel = QLabel(
            f"坐标系: {self.mapCanvas.mapSettings().destinationCrs().description()}-{self.mapCanvas.mapSettings().destinationCrs().authid()}")
        self.statusBar.addWidget(self.statusCrsLabel)

        self.setStatusBar(self.statusBar)

        # 9 error catch
        self.old_hook = sys.excepthook
        sys.excepthook = self.catch_exceptions

        # A 按钮、菜单栏功能
        self.connectFunc()




    def connectFunc(self):

        # 每次移动鼠标，坐标和比例尺变化
        self.mapCanvas.xyCoordinates.connect(self.showXY)
        self.mapCanvas.scaleChanged.connect(self.showScale)
        self.mapCanvas.destinationCrsChanged.connect(self.showCrs)
        self.statusScaleComboBox.editTextChanged.connect(self.changeScaleForString)

        # action
        self.actionOpenRaster.triggered.connect(self.actionOpenRasterTriggered)
        self.actionOpenVector.triggered.connect(self.actionOpenShpTriggered)

        self.actionConnect.triggered.connect(self.openDataBaseDialog)

    def showXY(self, point):
        x = point.x()
        y = point.y()
        self.statusXY.setText(f'{x:.6f}, {y:.6f}')

    def showScale(self, scale):
        self.statusScaleComboBox.setEditText(f"1:{int(scale)}")

    def showCrs(self):
        mapSetting: QgsMapSettings = self.mapCanvas.mapSettings()
        self.statusCrsLabel.setText(
            f"坐标系: {mapSetting.destinationCrs().description()}-{mapSetting.destinationCrs().authid()}")

    def changeScaleForString(self, str):
        try:
            left, right = str.split(":")[0], str.split(":")[-1]
            if int(left) == 1 and int(right) > 0 and int(right) != int(self.mapCanvas.scale()):
                self.mapCanvas.zoomScale(int(right))
                self.mapCanvas.zoomWithCenter()
        except:
            print(traceback.format_stack())

    def dragEnterEvent(self, fileData):
        if fileData.mimeData().hasUrls():
            fileData.accept()
        else:
            fileData.ignore()

    # 拖拽文件事件
    def dropEvent(self, fileData):
        mimeData: QMimeData = fileData.mimeData()
        filePathList = [u.path()[1:] for u in mimeData.urls()]
        for filePath in filePathList:
            filePath: str = filePath.replace("/", "//")
            if filePath.split(".")[-1] in ["tif", "TIF", "tiff", "TIFF", "GTIFF", "png", "jpg", "pdf"]:
                self.addRasterLayer(filePath)
            elif filePath.split(".")[-1] in ["shp", "SHP", "gpkg", "geojson", "kml"]:
                self.addVectorLayer(filePath)
            elif filePath == "":
                pass
            else:
                QMessageBox.about(self, '警告', f'{filePath}为不支持的文件类型，目前支持栅格影像和shp矢量')

    def catch_exceptions(self, ty, value, trace):

        traceback_format = traceback.format_exception(ty, value, trace)
        traceback_string = "".join(traceback_format)
        QMessageBox.about(self, 'error', traceback_string)
        self.old_hook(ty, value, trace)

    def actionOpenRasterTriggered(self):
        data_file, ext = QFileDialog.getOpenFileName(self, '打开', '','GeoTiff(*.tif;*tiff;*TIF;*TIFF);;All Files(*);;JPEG(*.jpg;*.jpeg;*.JPG;*.JPEG);;*.png;;*.pdf')
        if data_file:
            self.addRasterLayer(data_file)

    def actionOpenShpTriggered(self):
        data_file, ext = QFileDialog.getOpenFileName(self, '打开', '',"ShapeFile(*.shp);;All Files(*);;Other(*.gpkg;*.geojson;*.kml)")
        if data_file:
            self.addVectorLayer(data_file)

    def openDataBaseDialog(self):
        dialog = QDialog()
        ui = Ui_Dialog()
        ui.setupUi(dialog)

        ui.pushButton.clicked.connect(self.testConnection)

        dialog.exec_()

    def testConnection(self):
        print("Testing database connection...")
        dialog = self.sender().parent()
        name = dialog.findChild(QtWidgets.QLineEdit, "lineEdit").text()
        host = dialog.findChild(QtWidgets.QLineEdit, "lineEdit_2").text()
        port = dialog.findChild(QtWidgets.QLineEdit, "lineEdit_3").text()
        database = dialog.findChild(QtWidgets.QLineEdit, "lineEdit_4").text()
        print(f"Name: {name}, Host: {host}, Port: {port}, Database: {database}")

    # 添加栅格图层
    def addRasterLayer(self, rasterFilePath):
        rasterLayer = readRasterFile(rasterFilePath)
        if self.firstAdd:
            addMapLayer(rasterLayer, self.mapCanvas, True)
            self.firstAdd = False
        else:
            addMapLayer(rasterLayer, self.mapCanvas)

    # 添加矢量图层
    def addVectorLayer(self, vectorFilePath):
        vectorLayer = readVectorFile(vectorFilePath)
        if self.firstAdd:
            addMapLayer(vectorLayer, self.mapCanvas, True)
            self.firstAdd = False
        else:
            addMapLayer(vectorLayer, self.mapCanvas)
