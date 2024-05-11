import os
import sys
import json
import qdarkstyle
from PyQt5 import QtWidgets, QtGui, QtCore

from pages.list_building_items import ListBuildingItems
from pages.settings_tab import SettingsWidget


from utils.data_manager import DataManager

class SimCityCalculator(QtWidgets.QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.resize(800, 600)
        self.setWindowTitle("SimCity Calculator")

        self.tabs_list = []
        self.data_manager = DataManager()
        self.data = self.data_manager.get_data()
        self.data_manager.update_func = self._update_func

        self._create_widgets()
        self._create_layouts()

    def update_tabs(self):
        self.tabs.clear()
        self.tabs_list = []
        self._create_layouts()

    def _create_widgets(self):
        self.tabs = QtWidgets.QTabWidget()
        self.setCentralWidget(self.tabs)

    def _update_func(self):
        for item in self.tabs_list:
            item._update_func()

    def _create_layouts(self):
        for index, building in enumerate(self.data):
            item = ListBuildingItems(self, self.data_manager, index)
            self.tabs.addTab(item, building['name'])
            self.tabs_list.append(item)

        self.settings_tab = SettingsWidget(self.data_manager)
        self.tabs.addTab(self.settings_tab, "Settings")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    styles = QtWidgets.QStyleFactory.keys()
    app.setStyle(styles[2])
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())

    window = SimCityCalculator()
    window.show()

    sys.exit(app.exec())