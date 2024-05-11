import json
from PyQt5 import QtCore, QtWidgets, QtGui

from utils.constants import INCREMENT, DECREMENT
from utils.data_manager import DataManager

from pages.results_window import Results

class ListBuildingItems(QtWidgets.QWidget):
    def __init__(self, parent, data_manager:DataManager, index):
        super().__init__()
        self._building_index = index
        self._count_widgets = []
        self.test_label = QtWidgets.QLabel(text="test")

        self.data_manager:DataManager = data_manager
        self.data:dict = self.data_manager.get_data()
        self.parent = parent

        self._create_layouts()

    def _update_func(self):
        self.data = self.data_manager.get_data()
        for item_index, item in enumerate(self.data[self._building_index]['items']):
            self._count_widgets[item_index].setText(str(item['count']))

    def update_item(self, index:int, type:str):
        if type == INCREMENT:
            self.data[self._building_index]['items'][index]['count'] += 1
        elif type == DECREMENT:
            self.data[self._building_index]['items'][index]['count'] -= 1
        self.data_manager.update_data(self.data)
        self.data_manager.update_materials(self._building_index, index, type)

    def clear_all(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[i]['items'])):
                self.data[i]['items'][j]['count'] = 0
        self.data_manager.update_data(self.data)

    def clear_current(self):
        for j in range(len(self.data[self._building_index]['items'])):
            self.data[self._building_index]['items'][j]['count'] = 0
            self.data_manager.update_materials(self._building_index, j, DECREMENT)
        self.data_manager.update_data(self.data)

    def create_row(self, index:int, item:dict):
        child_frame = QtWidgets.QFrame()
        child_layout = QtWidgets.QHBoxLayout()

        name = QtWidgets.QLabel(text=item['name'])
        count = QtWidgets.QLabel(text=str(item['count']))
        add_btn = QtWidgets.QPushButton(text="Add")
        subtract_btn = QtWidgets.QPushButton(text="Remove")

        add_btn.clicked.connect(lambda: self.update_item(index, INCREMENT))
        subtract_btn.clicked.connect(lambda: self.update_item(index, DECREMENT))

        child_layout.addWidget(name, stretch=20, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        child_layout.addWidget(count, stretch=1, alignment=QtCore.Qt.AlignmentFlag.AlignLeft)
        child_layout.addWidget(add_btn, stretch=1, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        child_layout.addWidget(subtract_btn, stretch=1, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        self._count_widgets.append(count)
        child_frame.setLayout(child_layout)

        return child_frame
    
    def calculate(self):
        self.window = Results(self, self.data_manager)
        self.window.show()
    
    def create_bottom_buttons(self):
        layout = QtWidgets.QHBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        calculate_btn = QtWidgets.QPushButton(text="Calculate")
        calculate_btn.clicked.connect(lambda: self.calculate())

        clear_btn = QtWidgets.QPushButton(text="Clear Current")
        clear_btn.clicked.connect(lambda: self.clear_current())

        clear_all_btn = QtWidgets.QPushButton(text="Clear All")
        clear_all_btn.clicked.connect(lambda: self.clear_all())

        layout.addWidget(calculate_btn, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(clear_btn, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(clear_all_btn, alignment=QtCore.Qt.AlignmentFlag.AlignRight)

        return layout

    def _create_layouts(self):
        
        layout = QtWidgets.QVBoxLayout()

        list_layout = QtWidgets.QVBoxLayout()
        list_layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop)

        for index, item in enumerate(self.data[self._building_index]['items']):
            widget = self.create_row(index, item)
            list_layout.addWidget(widget)

        layout.addLayout(list_layout)
        layout.addLayout(self.create_bottom_buttons())
        self.setLayout(layout)
