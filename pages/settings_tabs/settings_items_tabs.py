from PyQt5 import QtWidgets, QtCore, QtGui
from utils.data_manager import DataManager

from pages.items_update_window import ItemUpdateWindow

class SettingsItemsTab(QtWidgets.QWidget):
    def __init__(self, data_manager:DataManager):
        super().__init__()

        self.data_manager = data_manager
        self.data = self.data_manager.get_data()

        self._curr_item_selected_building = 0
        self.selected_item = None

        self.items_list = []

    def update_list(self):
        self.data = self.data_manager.get_data()
        self.items_list_widget.clear()
        for item in self.data[self._curr_item_selected_building]['items']:
            list_item = QtWidgets.QListWidgetItem()
            list_item.setText(item['name'])
            self.items_list_widget.addItem(list_item)
            self.items_list.append(list_item)

    def update_building_dropdown(self, index):

        # update current building index
        self._curr_item_selected_building = index

        # update building items
        self.items_list_widget.clear()
        for item in self.data[self._curr_item_selected_building]['items']:
            list_item = QtWidgets.QListWidgetItem()
            list_item.setText(item['name'])
            self.items_list_widget.addItem(list_item)

    def _item_selected(self, item):
        index = self.items_list.index(item)
        self.selected_item = index
        self._items_update_btn.setDisabled(False)
        print(index)

    def add_item(self):
        self.window = ItemUpdateWindow(self, self.data_manager, self._curr_item_selected_building)
        self.window.show()

    def update_item(self):
        if self.selected_item is not None:
            self.window = ItemUpdateWindow(self, self.data_manager, self._curr_item_selected_building, self.selected_item)
            self.window.show()

    def delete_item(self):
        if self.selected_item is not None:
            del self.data[self._curr_item_selected_building]['items'][self.selected_item]
            self.data_manager.update_data(self.data)
            self.data_manager.update_func()
    
    def _create_items_tab(self):
        layout = QtWidgets.QVBoxLayout()
        sub_layout = QtWidgets.QHBoxLayout()

        self.items_list_widget = QtWidgets.QListWidget()
        buttons_layout = QtWidgets.QVBoxLayout()
        buttons_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        self._buildings_dropdown = QtWidgets.QComboBox()
        self._buildings_dropdown.addItems([ building['name'] for building in self.data ])
        self._buildings_dropdown.currentIndexChanged.connect(self.update_building_dropdown)

        sub_layout.addWidget(self.items_list_widget)
        sub_layout.addLayout(buttons_layout)
        layout.addWidget(self._buildings_dropdown)
        layout.addLayout(sub_layout)

        self._items_add_btn = QtWidgets.QPushButton(text="Add")
        self._items_update_btn = QtWidgets.QPushButton(text="Update")
        self._items_delete_btn = QtWidgets.QPushButton(text="Delete")

        self._items_update_btn.setDisabled(True)

        self._items_add_btn.clicked.connect(lambda: self.add_item())
        self._items_update_btn.clicked.connect(lambda: self.update_item())
        self._items_delete_btn.clicked.connect(lambda: self.delete_item())

        for item in self.data[self._curr_item_selected_building]['items']:
            list_item = QtWidgets.QListWidgetItem()
            list_item.setText(item['name'])
            self.items_list_widget.addItem(list_item)
            self.items_list.append(list_item)

        self.items_list_widget.itemClicked.connect(self._item_selected)

        buttons_layout.addWidget(self._items_add_btn),
        buttons_layout.addWidget(self._items_update_btn)
        buttons_layout.addWidget(self._items_delete_btn)

        return layout