from PyQt5 import QtWidgets, QtCore, QtGui
from utils.data_manager import DataManager

class ItemUpdateWindow(QtWidgets.QWidget):
    def __init__(self, parent, data_manager:DataManager, building_index, item=None):
        super().__init__()

        self.resize(300, 100)
        self.building_index = building_index
        self.item_index = item

        self.data_manager:DataManager = data_manager
        self.data = self.data_manager.get_data()
        self.parent = parent

        self._create_widgets()
        self._create_layouts()

    def _on_cancel_click(self):
        self.close()

    def _on_save_click(self):
        name = self.name_input.text()
        if not len(name.strip()):
            return
        
        if self.item_index is not None:
            self.data[self.building_index]['items'][self.item_index]['name'] = name
        else:
            self.data[self.building_index]['items'].append(
                { "name": name, "materials": [], "count": 0 }
            )

        self.data_manager.update_data(self.data)
        self.data_manager.update_func()
        self.parent.update_list()
        self.close()

    def _create_widgets(self):
        self.name_label = QtWidgets.QLabel(text="Name")
        self.name_input = QtWidgets.QLineEdit()

        if self.item_index is not None:
            self.name_input.setText(self.data[self.building_index]['items'][self.item_index]['name'])

        self.save_btn = QtWidgets.QPushButton(text="Save")
        self.cancel_btn = QtWidgets.QPushButton(text="Cancel")

        self.save_btn.clicked.connect(lambda: self._on_save_click())
        self.cancel_btn.clicked.connect(lambda: self._on_cancel_click())

    def _create_layouts(self):
        layout = QtWidgets.QVBoxLayout()
        
        form_layout = QtWidgets.QFormLayout()
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        form_layout.addRow(self.name_label, self.name_input)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)
