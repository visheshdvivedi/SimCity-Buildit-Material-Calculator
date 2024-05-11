import json
from utils.constants import INCREMENT, DECREMENT

class DataManager:
    def __init__(self) -> None:
        self._data = []

        with open("data.json", "r+") as file:
            self._data = json.loads(file.read())

        self.update_func:function = None

    def get_data(self):
        return self._data
    
    def update_data(self, data:dict):
        with open("data.json", "w+") as file:
            file.write(json.dumps(data))

        with open("data.json", "r+") as file:
            self._data = json.loads(file.read())

        self.update_func()

    def update_materials(self, building_index:int, item_index:int, type:str):
        for material in self._data[building_index]['items'][item_index]['materials']:
            if type == INCREMENT:
                self._data[material['building_index']]['items'][material['item_index']]['count'] += int(material['count'])
                if material['building_index'] != 0:
                    self.update_materials(material['building_index'], material['item_index'], type)
            elif type == DECREMENT:
                self._data[material['building_index']]['items'][material['item_index']]['count'] -= int(material['count'])
                if material['building_index'] != 0:
                    self.update_materials(material['building_index'], material['item_index'], type)
        self.update_data(self._data)