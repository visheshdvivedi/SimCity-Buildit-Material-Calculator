from PyQt5 import QtWidgets, QtCore, QtGui
from utils.data_manager import DataManager

from pages.material_update_window import MaterialUpdateWindow

class SettingsMaterialsTab(QtWidgets.QWidget):
    def __init__(self, data_manager:DataManager):
        super().__init__()

        self.data_manager = data_manager
        self.data = self.data_manager.get_data()

        self._curr_selected_item_building = 0
        self._curr_selected_item = 0
        self.selected_material = None

        self.materials_list = []

        self._building_dropdown = QtWidgets.QComboBox()
        self._items_dropdown = QtWidgets.QComboBox()

    def update_list(self):
        self.data = self.data_manager.get_data()
        self.materials_list_widget.clear()
        for material in self.data[self._curr_selected_item_building]['items'][self._curr_selected_item]['materials']:
            list_item = QtWidgets.QListWidgetItem()
            list_item.setText(self.data[material['building_index']]['items'][material['item_index']]['name'] + f"({str(material['count'])})")
            self.materials_list_widget.addItem(list_item)
            self.materials_list.append(list_item)

    def update_building_dropdown_index(self, building_index):
        self._curr_selected_item_building = building_index

        self._items_dropdown.clear()
        self._items_dropdown.addItems([ item['name'] for item in self.data[self._curr_selected_item_building]['items'] ])

    def update_item_dropdown_index(self, item_index):

        self._curr_selected_item = item_index

        # update item materials
        self.materials_list_widget.clear()
        for material in self.data[self._curr_selected_item_building]['items'][self._curr_selected_item]['materials']:
            list_item = QtWidgets.QListWidgetItem()
            list_item.setText(self.data[material['building_index']]['items'][material['item_index']]['name'] + f"({str(material['count'])})")
            self.materials_list_widget.addItem(list_item)
            self.materials_list.append(list_item)

    def _materials_selected(self, item):
        index = self.materials_list.index(item)
        self.selected_material = index
        self._materials_update_btn.setDisabled(False)

    def add_materials(self):
        self.window = MaterialUpdateWindow(self, self.data_manager, self._curr_selected_item_building, self._curr_selected_item)
        self.window.show()

    def update_materials(self):
        if self.selected_material is not None:
            material_details = self.data[self._curr_selected_item_building]['items'][self._curr_selected_item]['materials'][self.selected_material]
            material_details['index'] = self.selected_material
            self.window = MaterialUpdateWindow(self, self.data_manager, self._curr_selected_item_building, self._curr_selected_item, material_details)
            self.window.show()

    def delete_materials(self):
        if self.selected_material is not None:
            print(self._curr_selected_item_building, self._curr_selected_item, self.selected_material)
            del self.data[self._curr_selected_item_building]['items'][self._curr_selected_item]['materials'][self.selected_material]
            self.data_manager.update_data(self.data)
            self.data_manager.update_func()
    
    def _create_materials_tab(self):
        layout = QtWidgets.QVBoxLayout()
        sub_layout = QtWidgets.QHBoxLayout()

        self.materials_list_widget = QtWidgets.QListWidget()
        buttons_layout = QtWidgets.QVBoxLayout()
        buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self._building_dropdown.currentIndexChanged.connect(self.update_building_dropdown_index)
        self._building_dropdown.addItems([building['name'] for building in self.data])

        self._items_dropdown.currentIndexChanged.connect(self.update_item_dropdown_index)
        self._items_dropdown.addItems([ item['name'] for item in self.data[self._curr_selected_item_building]['items'] ])

        sub_layout.addWidget(self.materials_list_widget)
        sub_layout.addLayout(buttons_layout)

        layout.addWidget(self._building_dropdown)
        layout.addWidget(self._items_dropdown)
        layout.addLayout(sub_layout)

        self._materials_add_btn = QtWidgets.QPushButton(text="Add")
        self._materials_update_btn = QtWidgets.QPushButton(text="Update")
        self._materials_delete_btn = QtWidgets.QPushButton(text="Delete")

        self._materials_update_btn.setDisabled(True)

        self._materials_add_btn.clicked.connect(lambda: self.add_materials())
        self._materials_update_btn.clicked.connect(lambda: self.update_materials())
        self._materials_delete_btn.clicked.connect(lambda: self.delete_materials())

        for material in self.data[self._curr_selected_item_building]['items'][self._curr_selected_item]['materials']:
            list_item = QtWidgets.QListWidgetItem()
            list_item.setText(self.data[material['building_index']]['items'][material['item_index']]['name'] + f"({str(material['count'])})")
            self.materials_list_widget.addItem(list_item)
            self.materials_list.append(list_item)

        self.materials_list_widget.itemClicked.connect(self._materials_selected)

        buttons_layout.addWidget(self._materials_add_btn),
        buttons_layout.addWidget(self._materials_update_btn)
        buttons_layout.addWidget(self._materials_delete_btn)

        return layout