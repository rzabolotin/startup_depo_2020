import sys

import numpy as np
import pyqtgraph as pg
import qdarkstyle
from matplotlib import image
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtWidgets import QFileDialog

from main_logic import MainLogic
import gaps_detection


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.logic = MainLogic()

        self.setWindowFlags(QtCore.Qt.Window)
        self.setWindowTitle("Defect Detector")
        self.open_avi_action = QtWidgets.QAction("Open video...")
        self.open_avi_action.triggered.connect(self.open_avi)
        self.open_csv_action = QtWidgets.QAction("Open CSV...")
        self.open_csv_action.triggered.connect(self.open_csv)
        self.open_csv_action.setShortcut("Ctrl+O")

        self.menuBar().addAction(self.open_avi_action)
        self.menuBar().addAction(self.open_csv_action)

        self.gaps_list = QtWidgets.QListView()
        self.gaps_model = QtGui.QStandardItemModel()
        self.gaps_list.setModel(self.gaps_model)
        self.gaps_list.pressed["const QModelIndex&"].connect(self.on_select_element)
        self.gaps_list.activated["const QModelIndex&"].connect(self.on_select_element)

        self.info_label = QtWidgets.QLabel("Мин. зазор, мм")
        self.gap_limit_spinbox = QtWidgets.QSpinBox()
        self.gap_limit_spinbox.setRange(0, 1000)
        self.gap_limit_spinbox.setValue(0)
        self.gap_limit_spinbox.setSingleStep(1)
        self.gap_limit_spinbox.valueChanged["int"].connect(self.change_gap_limit)
        self.rail_combo = QtWidgets.QComboBox()
        self.rail_combo.addItems(self.logic.RAILS)
        self.rail_combo.currentIndexChanged["int"].connect(self.change_rail_combo)

        self.hbox_filter = QtWidgets.QHBoxLayout()
        self.hbox_filter.addWidget(self.info_label, stretch=0)
        self.hbox_filter.addWidget(self.gap_limit_spinbox, stretch=10)
        self.hbox_filter.addWidget(self.rail_combo, stretch=10)

        self.vbox_data = QtWidgets.QVBoxLayout()
        self.vbox_data.addLayout(self.hbox_filter)
        self.vbox_data.addWidget(self.gaps_list)
        self.board_widget = QtWidgets.QWidget()
        self.board_widget.setLayout(self.vbox_data)

        self.plot_area = self.create_plot_area(self)
        self.image_item = pg.ImageItem()
        self.plot_area.addItem(self.image_item)

        self.plot_area_nn = self.create_plot_area(self)
        self.image_item_nn = pg.ImageItem()
        self.plot_area_nn.addItem(self.image_item_nn)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.board_widget)
        self.splitter2 = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        self.splitter2.addWidget(self.plot_area)
        self.splitter2.addWidget(self.plot_area_nn)
        self.splitter.addWidget(self.splitter2)

        self.vbox = QtWidgets.QVBoxLayout(self)
        self.vbox.addWidget(self.splitter)
        self.setCentralWidget(QtWidgets.QWidget(self))
        self.centralWidget().setLayout(self.vbox)
        self.showMaximized()

        self.rectangle_region = None

    def create_plot_area(self, plot_area):
        plot_area = pg.PlotWidget()
        plot_area.setCursor(QtCore.Qt.CrossCursor)
        plot_area.setMenuEnabled(False)
        plot_area.scene().sigMouseClicked.connect(self.mouse_clicked)
        plot_area.scene().sigMouseMoved.connect(self.mouse_moved)
        plot_area.getPlotItem().getAxis('bottom').enableAutoSIPrefix(False)
        plot_area.getPlotItem().getAxis('left').enableAutoSIPrefix(False)
        plot_area.getPlotItem().hideAxis('bottom')
        plot_area.getPlotItem().hideAxis('left')
        plot_area.setAspectLocked(True)
        return plot_area
        
    def open_avi(self, checked):
        file_name1, _ = QFileDialog.getOpenFileName(parent=self, caption="Открыть первый AVI файл", filter="AVI (*.avi)",
                                                    directory="data")
        file_name2, _ = QFileDialog.getOpenFileName(parent=self, caption="Открыть второй AVI файл", filter="AVI (*.avi)",
                                                    directory="data")
        cadr_count, ok = QtWidgets.QInputDialog.getInt(self, "Defect Detector", "Остановиться после N стыков:")
        if file_name1 and file_name2 and ok:
            from splash import Splash
            splash = Splash()
            splash.set_message("Поиск")
            csv_file_name = self.logic.open_avi(file_name1, file_name2, cadr_count)
            splash.close_message(self)
            print(csv_file_name)
            if csv_file_name:
                self.logic.open_csv(csv_file_name)
                self.refresh_gaps_list()

    def open_csv(self, checked):
        file_name, _ = QFileDialog.getOpenFileName(parent=self, caption="Открыть CSV файл", filter="CSV (*.csv)",
                                                   directory="data")
        if file_name:
            if self.logic.open_csv(file_name):
                self.refresh_gaps_list()

    def refresh_gaps_list(self):
        if self.logic.df_gaps is None:
            return
        self.gaps_model.clear()
        self.logic.filter()
        for i, (index, row) in enumerate(self.logic.filter_df_gaps.iterrows()):
            item = QtGui.QStandardItem(f"({row['rail']}) {row['kilometer']} км {row['meter']} м: зазор {row['gap']} мм (кадр {row['cadr']})")
            item.setEditable(False)
            self.gaps_model.appendRow(item)
            index = self.gaps_model.indexFromItem(item)
            self.gaps_model.setData(index, i, role=QtCore.Qt.UserRole)
        self.gaps_list.setModel(self.gaps_model)

    def on_select_element(self, index):
        num = index.data(QtCore.Qt.UserRole)
        self.draw_image(num, "file_name", self.image_item)
        self.draw_image_nn(num, "file_name", self.image_item_nn)

    def draw_image(self, num, file_name_key, image_item):
        image_file_name = self.logic.folder + "/" + self.logic.filter_df_gaps[file_name_key].values[num]
        img = image.imread(image_file_name)
        img = np.swapaxes(img, 0, 1)
        img = img[:, ::-1, :]
        image_item.setImage(img)

    def draw_image_nn(self, num, file_name_key, image_item):
        image_file_name = self.logic.folder + "//data_nn//" + self.logic.filter_df_gaps[file_name_key].values[num]
        img = image.imread(image_file_name)
        img = np.swapaxes(img, 0, 1)
        img = img[:, ::-1, :]
        image_item.setImage(img)


    def mouse_clicked(self, evt):
        pnt = evt.scenePos()
        pnt = (pnt.x(), pnt.y())
        mouse_point = self.plot_area.getPlotItem().vb.mapSceneToView(evt.scenePos())
        x = mouse_point.x()
        y = mouse_point.y()
        btn = evt.button()
        print(x, y)

    def mouse_moved(self, evt):
        pass

    def change_rail_combo(self, value):
        if value == -1:
            return
        self.logic.current_rail = self.logic.RAILS[value]
        self.refresh_gaps_list()

    def change_gap_limit(self, value):
        self.logic.gap_limit = int(value)
        self.refresh_gaps_list()


def config_pyqtgraph():
    pg.setConfigOption("antialias", True)
    pg.setConfigOption("leftButtonPan", True)
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')


if __name__ == "__main__":
    # config_pyqtgraph()
    from PyQt5.QtWidgets import QApplication
    QApplication.setAttribute(QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window = MainWindow()
    window.show()
    app.exec()
