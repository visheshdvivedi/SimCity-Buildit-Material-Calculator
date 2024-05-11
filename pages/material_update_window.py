from PyQt5 import QtWidgets, QtCore, QtGui
from utils.data_manager import DataManager

class MaterialUpdateWindow(QtWidgets.QWidget):
    def __init__(self, parent, data_manager:DataManager, building_index, item_index, material_details=None):
        super().__init__()

        self.resize(300, 100)
        self.building_index = building_index
        self.item_index = item_index
        self.material_details = material_details

        self.data_manager:DataManager = data_manager
        self.data = self.data_manager.get_data()
        self.parent = parent

        self._create_widgets()
        self._create_layouts()

    def _on_cancel_click(self):
        self.close()

    def _on_save_click(self):
        
        if self.material_details is not None:
            self.data[self.building_index]['items'][self.item_index]['materials'][self.material_details['index']] = {
                "building_index": self.building_input.currentIndex(),
                "item_index": self.item_input.currentIndex(),
                "count": self.count_input.text()
            }
        else:
            self.data[self.building_index]['items'][self.item_index]['materials'].append({
                "building_index": self.building_input.currentIndex(),
                "item_index": self.item_input.currentIndex(),
                "count": self.count_input.text()
            })

        self.data_manager.update_data(self.data)
        self.data_manager.update_func()
        self.parent.update_list()
        self.close()

    def update_building_input(self, index):
        self.item_input.clear()
        self.item_input.addItems([item['name'] for item in self.data[index]['items']])

    def _create_widgets(self):
        self.building_label = QtWidgets.QLabel(text="Building")
        self.building_input = QtWidgets.QComboBox()
        self.building_input.addItems([building['name'] for building in self.data])
        self.building_input.currentIndexChanged.connect(self.update_building_input)

        self.item_label = QtWidgets.QLabel(text="Item")
        self.item_input = QtWidgets.QComboBox()
        self.item_input.addItems([item['name'] for item in self.data[self.building_input.currentIndex()]['items']])

        self.count_label = QtWidgets.QLabel(text="Count")
        self.count_input = QtWidgets.QLineEdit()
        
        validator = QtGui.QIntValidator(bottom=1, top=5)
        self.count_input.setValidator(validator)

        if self.material_details is not None:
            self.building_input.setCurrentIndex(self.material_details['building_index'])
            self.item_input.setCurrentIndex(self.material_details['item_index'])
            self.count_input.setText(str(self.material_details['count']))

        self.save_btn = QtWidgets.QPushButton(text="Save")
        self.cancel_btn = QtWidgets.QPushButton(text="Cancel")

        self.save_btn.clicked.connect(lambda: self._on_save_click())
        self.cancel_btn.clicked.connect(lambda: self._on_cancel_click())

    def _create_layouts(self):
        layout = QtWidgets.QVBoxLayout()
        
        form_layout = QtWidgets.QFormLayout()
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        form_layout.addRow(self.building_label, self.building_input)
        form_layout.addRow(self.item_label, self.item_input)
        form_layout.addRow(self.count_label, self.count_input)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)
