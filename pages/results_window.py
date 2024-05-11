from PyQt5 import QtWidgets, QtCore, QtGui
from utils.data_manager import DataManager

class Results(QtWidgets.QWidget):
    def __init__(self, parent, data_manager:DataManager):
        super().__init__()

        self.resize(300, 500)
        self.data_manager: DataManager = data_manager

        self._create_widgets()
        self._create_layout()

    def _create_widgets(self):
        self._list_item_widget = QtWidgets.QListWidget()
        self._list_items = []
        data = self.data_manager.get_data()

        for building in data:
            for item in building['items']:
                if item['count'] > 0:
                    self._list_items.append(f"{item['name']} ({item['count']})")

        self._list_item_widget.addItems(self._list_items)
        self._label = QtWidgets.QLabel(text="Here are the items you wanna make")
        

    def _create_layout(self):
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self._label)
        layout.addWidget(self._list_item_widget)
        self.setLayout(layout)