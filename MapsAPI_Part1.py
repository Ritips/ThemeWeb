from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QInputDialog, QPushButton
from PyQt5.QtGui import QPixmap, QFontMetrics
from PyQt5.Qt import Qt
import requests
import math
import sys


class ShowMap(QWidget):
    def __init__(self):
        super(ShowMap, self).__init__()
        self.setGeometry(500, 200, 900, 600)
        self.setWindowTitle('Map')

        self.image = QLabel('', self)
        self.image.setGeometry(25, 50, 600, 450)
        self.image.setStyleSheet("background-color: white;"
                                 "border-style: outset;"
                                 "border-width: 1px;"
                                 "border-color: black;")

        self.pixmap = QPixmap()
        self.address = QLabel('Address: ', self)
        self.address.setGeometry(25, 10, 600, 35)
        self.address.setStyleSheet("background-color: white;"
                                   "border-style: outset;"
                                   "border-width: 2px;"
                                   "border-radius: 10px;"
                                   "border-color: black;"
                                   "font: bold 12px;")
        self.map_center = (325, 275)
        self.address_text = None
        self.address_only = None
        self.default_toponym_point = self.toponym_point = self.toponym = self.spn = self.default_spn = None
        self.par_l = 'map'
        self.get_name = ''
        self.scale_size = 0.05
        self.scale_ll = 0.05
        self.show_post_index = False
        self.btn_map = QPushButton('Show map', self)
        self.btn_scale = QPushButton('Set Scale of Size', self)
        self.btn_scale_ll = QPushButton("Self scale of movement", self)
        self.btn_scheme = QPushButton("Set Scheme", self)
        self.btn_reset = QPushButton("Reset point", self)
        self.btn_post = QPushButton("Show PostIndex ({0})".format(self.show_post_index), self)

        buttons = [self.btn_map, self.btn_scale, self.btn_scale_ll, self.btn_scheme, self.btn_reset, self.btn_post]
        for i in range(len(buttons)):
            buttons[i].setFocusPolicy(Qt.NoFocus)
            buttons[i].setGeometry(650, 50 * (1 + i) + 10 * i, 200, 50)
            buttons[i].setStyleSheet("background-color: white;"
                                     "border-style: outset;"
                                     "border-width: 2px;"
                                     "border-radius: 10px;"
                                     "border-color: black;"
                                     "font: bold 14px;")

        self.btn_map.clicked.connect(self.get_address)
        self.btn_scale.clicked.connect(self.set_scale)
        self.btn_scale_ll.clicked.connect(self.set_scale_ll)
        self.btn_scheme.clicked.connect(self.set_par_l)
        self.btn_reset.clicked.connect(self.reset_point)
        self.btn_post.clicked.connect(self.set_post_index)

        self.setMouseTracking(True)
        self.show_pt = True

    def mousePressEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        if not self.toponym_point:
            return
        if 25 < x < 625 and 50 < y < 500:
            print(self.toponym_point, (x, y), self.spn)
            print(self.toponym_point[0] * self.spn[0] * 600 / 360)
            print(self.toponym_point[1] * self.spn[1] * 450 / 180)
            lat = self.toponym_point[1]
            lng = self.toponym_point[0]
            sin_y = math.sin((lat * math.pi) / 180)
            sin_y = min(max(sin_y, -0.9999), 0.9999)
            some_num = self.spn[0] * 256 * (0.5 - math.log((1 + sin_y / (1 - sin_y)) / (4 * math.pi)))
            another_num = self.spn[1] * 256 * (0.5 + lng / 360)
            print(some_num, another_num)

    def reset_point(self):
        if self.show_pt and self.get_name:
            self.show_pt = False
            self.address_text = 'Address: '
            self.address.setText(self.address_text)
            self.get_image()

    def set_post_index(self):
        self.show_post_index = True if not self.show_post_index else False
        self.btn_post.setText("Show PostIndex ({0})".format(self.show_post_index))
        if not self.toponym:
            return
        if self.show_post_index and self.get_name and self.show_pt:
            self.address_text = self.address.text() + ' ' + self.get_post_index()
        else:
            self.address_text = self.address_only
        self.address.setText(self.address_text)

    def set_par_l(self):
        sat_options = ['sat', 'sat,skl', 'sat,skl,trf', 'sat,trf']
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

    def set_address_text(self):
        text_size_finder = QFontMetrics(self.address.font())
        text_size = text_size_finder.width(self.address_text)
        if text_size > self.address.size().width():
            self.address.resize(text_size + 10, self.address.size().height())
        else:
            self.address.resize(600, 35)
        self.address.setText(self.address_text)

    def update(self):
        self.image.setPixmap(self.pixmap)

    def get_address(self):
        valid = QInputDialog.getText(self, "Address", "Input address")
        if not valid[1]:
            return
        self.get_name = valid[0]
        self.get_toponym(self.get_name)
        if not self.toponym:
            return
        self.get_coordinates(self.toponym)
        self.get_spn()
        self.show_pt = True
        self.get_image()

    def get_post_index(self):
        try:
            return self.toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['postal_code']
        except KeyError:
            return '(NO POST INDEX)'

    def get_image(self):
        if not self.toponym:
            return
        toponym_point = self.toponym_point
        par_l = self.par_l
        delta = self.spn
        map_params = {
            "ll": f"{toponym_point[0]},{toponym_point[1]}",
            "spn": f"{delta[0]},{delta[1]}",
            "l": par_l,
        }
        if self.show_pt:
            map_params["pt"] = f"{self.default_toponym_point[0]},{self.default_toponym_point[1]},round"
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
        amount_results = json_object["response"]["GeoObjectCollection"]["metaDataProperty"]["GeocoderResponseMetaData"]
        if not int(amount_results["found"]):
            self.address.setText(f"request: {amount_results['request']}; found; {amount_results['found']}")
            return
        self.toponym = json_object["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        self.address_text = self.toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["formatted"]
        self.address_only = self.address_text
        if self.show_post_index:
            self.address_text = self.address_text + ' ' + self.get_post_index()
        self.set_address_text()

    def get_coordinates(self, toponym):
        if not self.toponym:
            return
        self.toponym_point = tuple(map(float, toponym["Point"]["pos"].split()))
        self.default_toponym_point = self.toponym_point

    def get_spn(self):
        if not self.toponym:
            return
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
