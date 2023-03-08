from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QInputDialog, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.Qt import Qt
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
        self.default_toponym_point = self.toponym_point = self.toponym = self.spn = self.default_spn = None
        self.par_l = 'map'
        self.get_name = ''
        self.scale_size = 0.05
        self.scale_ll = 0.05

        self.button = QPushButton('Show map', self)
        self.button.setGeometry(650, 50, 150, 50)
        self.button.clicked.connect(self.get_address)
        self.button.setFocusPolicy(Qt.NoFocus)

        self.button_scale = QPushButton('Set Scale of Size', self)
        self.button_scale.setGeometry(650, 110, 150, 50)
        self.button_scale.clicked.connect(self.set_scale)
        self.button_scale.setFocusPolicy(Qt.NoFocus)

        self.button_scale_ll = QPushButton("Self scale of movement", self)
        self.button_scale_ll.setGeometry(650, 170, 150, 50)
        self.button_scale_ll.clicked.connect(self.set_scale_ll)
        self.button_scale_ll.setFocusPolicy(Qt.NoFocus)

        self.button_spn = QPushButton("Set Scheme", self)
        self.button_spn.setGeometry(650, 230, 150, 50)
        self.button_spn.clicked.connect(self.set_par_l)
        self.button_spn.setFocusPolicy(Qt.NoFocus)

    def set_par_l(self):
        sat_options = ['sat', 'sat,skl', 'sat,trf,skl', 'sat,trf']
        map_options = ['map', 'map,skl', 'map,skl,trf', 'map,trf']
        options = map_options + sat_options
        valid = QInputDialog.getItem(self, 'Scheme', 'Sat Scheme', options)
        if valid[1]:
            self.par_l = valid[0]
        else:
            self.par_l = 'map'
        if self.get_name:
            self.get_image()

    def set_scale(self):
        valid = QInputDialog.getText(self, 'Scale', 'SetScale')
        if not valid[1]:
            self.scale_size = 0.05
        else:
            try:
                self.scale_size = float(valid[0].replace(',', '.'))
            except ValueError:
                self.scale_size = 0.05

    def set_scale_ll(self):
        valid = QInputDialog.getText(self, 'Scale', 'SetScale')
        if not valid[1]:
            self.scale_ll = 0.05
        else:
            try:
                self.scale_ll = float(valid[0].replace(',', '.'))
            except ValueError:
                self.scale_ll = 0.05

    def keyPressEvent(self, event):
        key = event.key()
        if key in (16777238, 16777239):
            if not self.spn:
                return
            if key == 16777238:  # PAGE_UP
                x, y = self.spn
                x -= self.scale_size
                y -= self.scale_size
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0
                self.spn = (x, y)
            elif key == 16777239:  # PAGE_DOWN
                x, y = self.spn
                x += self.scale_size
                y += self.scale_size
                if x > self.default_spn[0] * 20:
                    x -= self.scale_size
                if y > self.default_spn[1] * 20:
                    y -= self.scale_size
                self.spn = (x, y)
            self.get_image()
            self.update()
        if key in (16777235, 16777237, 16777234, 16777236):
            if not self.toponym_point:
                return
            x, y = self.toponym_point
            if key == 16777234:  # Key_Left
                x -= self.scale_ll
                if x < 0:
                    x = self.scale_ll
            elif key == 16777235:  # Key_Up
                y += self.scale_ll
            elif key == 16777236:  # Key_Right
                x += self.scale_ll
            elif key == 16777237:  # Key_Down
                y -= self.scale_ll
                if y < 0:
                    y = self.scale_ll
            self.toponym_point = (x, y)
            self.get_image()
            self.update()

    def update(self):
        self.image.setPixmap(self.pixmap)

    def get_address(self):
        valid = QInputDialog.getText(self, "Address", "Input address")
        if not valid[1]:
            return
        self.get_name = valid[0]
        self.get_toponym(self.get_name)
        self.get_coordinates(self.toponym)
        self.get_spn()
        self.get_image()

    def get_image(self):
        toponym_point = self.toponym_point
        par_l = self.par_l
        delta = self.spn
        map_params = {
            "ll": f"{toponym_point[0]},{toponym_point[1]}",
            "spn": f"{delta[0]},{delta[1]}",
            "l": par_l,
            "pt": f"{self.default_toponym_point[0]},{self.default_toponym_point[1]},round"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        if not response:
            print(response, response.reason)
            print(response.url)
            return
        self.pixmap = QPixmap()
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
        self.default_toponym_point = self.toponym_point

    def get_spn(self):
        envelope = self.toponym["boundedBy"]["Envelope"]
        lower_corner = tuple(map(float, envelope["lowerCorner"].split()))
        upper_corner = tuple(map(float, envelope["upperCorner"].split()))
        self.spn = (abs(lower_corner[0] - upper_corner[0]), abs(lower_corner[1] - upper_corner[1]))
        self.default_spn = self.spn


if __name__ == "__main__":
    app = QApplication(sys.argv)
    exe = ShowMap()
    exe.show()
    sys.exit(app.exec_())
