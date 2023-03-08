from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QInputDialog, QPushButton
from PyQt5.QtGui import QPixmap
import requests
import sys


class ShowMap(QWidget):
    def __init__(self):
        super(ShowMap, self).__init__()
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Map')

        self.image = QLabel('', self)
        self.image.setGeometry(25, 50, 600, 450)
        self.image.setStyleSheet("background-color:white")

        self.pixmap = QPixmap()
        self.map_image = None
        self.get_name = ''
        self.toponym = None
        self.toponym_point = None
        self.button = QPushButton('Show map', self)
        self.button.setGeometry(650, 50, 100, 50)
        self.button.clicked.connect(self.get_address)

    def get_address(self):
        self.get_name = QInputDialog.getText(self, "Address", "Input address")[0]
        self.get_toponym(self.get_name)
        self.get_coordinates(self.toponym)
        self.get_image()

    def get_image(self, toponym_point=None, delta=(0.05, 0.05), par_l='map'):
        toponym_point = self.toponym_point if not toponym_point else toponym_point
        map_params = {
            "ll": f"{toponym_point[0]},{toponym_point[1]}",
            "spn": f"{delta[0]},{delta[1]}",
            "l": par_l,
            "pt": f"{toponym_point[0]},{toponym_point[1]},round"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        if not response:
            print(response, response.reason)
            print(response.url)
            return
        self.pixmap.loadFromData(response.content)
        self.image.setPixmap(self.pixmap)

    def get_toponym(self, toponym_to_find):
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            print(response, response.url)
            return
        json_object = response.json()
        self.toponym = json_object["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]

    def get_coordinates(self, toponym):
        self.toponym_point = tuple(map(float, toponym["Point"]["pos"].split()))

    def get_spn(self):
        envelope = self.toponym["boundedBy"]["Envelope"]
        lower_corner = tuple(map(float, envelope["lowerCorner"].split()))
        upper_corner = tuple(map(float, envelope["upperCorner"].split()))
        return abs(lower_corner[0] - upper_corner[0]), abs(lower_corner[1] - upper_corner[1])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exe = ShowMap()
    exe.show()
    sys.exit(app.exec_())
