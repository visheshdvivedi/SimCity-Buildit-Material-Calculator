from PyQt5 import QtWidgets, QtCore, QtGui
from utils.data_manager import DataManager

from pages.settings_tabs.settings_building_tabs import SettingsBuildingTab
from pages.settings_tabs.settings_items_tabs import SettingsItemsTab
from pages.settings_tabs.settings_materials_tabs import SettingsMaterialsTab

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self, data_manager:DataManager):
        super().__init__()

        self.tabs = QtWidgets.QTabWidget()

        self.data_manager:DataManager = data_manager
        self.data:dict = self.data_manager.get_data()

        self.building_tab_widget = SettingsBuildingTab(self.data_manager)
        self.items_tab_widget = SettingsItemsTab(self.data_manager)
        self.materials_tab_widget = SettingsMaterialsTab(self.data_manager)

        self._create_tabs()
        self._create_widgets()
        self._create_layout()

    def _update_func(self):
        self.building_tab_widget.building_list_widget.clear()
        for building in self.data:
            list_item = QtWidgets.QListWidgetItem()
            list_item.setText(building['name'])
            self.building_tab_widget.building_list_widget.addItem(list_item)
            self.building_tab_widget.building_items_list.append(list_item)

    def _create_tabs(self):
        self.buildings_tab = QtWidgets.QFrame()
        self.tabs.addTab(self.buildings_tab, "Buildings")
        self.items_tab = QtWidgets.QFrame()
        self.tabs.addTab(self.items_tab, "Items")
        self.materials_tab = QtWidgets.QFrame()
        self.tabs.addTab(self.materials_tab, "Materials")
        self.appearance_tab = QtWidgets.QFrame()
        self.tabs.addTab(self.appearance_tab, "Appearance")

    def _create_widgets(self):

        self.buildings_tab.setLayout(self.building_tab_widget._create_buildings_tab())
        self.items_tab.setLayout(self.items_tab_widget._create_items_tab())
        self.materials_tab.setLayout(self.materials_tab_widget._create_materials_tab())

    def _create_layout(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tabs)
        self.setLayout(layout)
