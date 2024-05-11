from PyQt5 import QtWidgets, QtCore, QtGui
from utils.data_manager import DataManager
from pages.building_update_window import BuildingUpdateWindow

class SettingsBuildingTab(QtWidgets.QWidget):
    def __init__(self, data_manager:DataManager):
        super().__init__()

        self.data_manager = data_manager
        self.data = self.data_manager.get_data()

        self.selected_building = None
        self.building_items_list = []

    def update_list(self):
        self.data = self.data_manager.get_data()
        self.building_items_list.clear()
        for building in self.data:
            list_item = QtWidgets.QListWidgetItem()
            list_item.setText(building['name'])
            self.building_list_widget.addItem(list_item)
            self.building_items_list.append(list_item)

    def _building_item_selected(self, item):
        index = self.building_items_list.index(item)
        self.selected_building = index
        self._building_update_btn.setDisabled(False)

    def add_building(self):
        self.window = BuildingUpdateWindow(self, self.data_manager)
        self.window.show()

    def update_building(self):
        if self.selected_building is not None:
            self.window = BuildingUpdateWindow(self, self.data_manager, self.selected_building)
            self.window.show()

    def delete_building(self):
        if self.selected_building is not None:
            del self.data[self.selected_building]
            self.data_manager.update_data(self.data)

    def _create_buildings_tab(self):
        layout = QtWidgets.QHBoxLayout()

        self.building_list_widget = QtWidgets.QListWidget()
        buttons_layout = QtWidgets.QVBoxLayout()
        buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self._building_add_btn = QtWidgets.QPushButton(text="Add")
        self._building_update_btn = QtWidgets.QPushButton(text="Update")
        self._building_delete_btn = QtWidgets.QPushButton(text="Delete")

        self._building_add_btn.clicked.connect(lambda: self.add_building())
        self._building_update_btn.clicked.connect(lambda: self.update_building())
        self._building_delete_btn.clicked.connect(lambda: self.delete_building())
        self._building_update_btn.setDisabled(True)

        for building in self.data:
            list_item = QtWidgets.QListWidgetItem()
            list_item.setText(building['name'])
            self.building_list_widget.addItem(list_item)
            self.building_items_list.append(list_item)

        self.building_list_widget.itemClicked.connect(self._building_item_selected)

        layout.addWidget(self.building_list_widget)
        layout.addLayout(buttons_layout)

        buttons_layout.addWidget(self._building_add_btn)
        buttons_layout.addWidget(self._building_update_btn)
        buttons_layout.addWidget(self._building_delete_btn)

        return layout