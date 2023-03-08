import requests
import sys
from io import BytesIO
from PIL import Image


def get_toponym(toponym_to_find):
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
    return json_object["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]


def get_point(toponym):
    return tuple(map(float, toponym["Point"]["pos"].split()))


def get_spn(toponym):
    envelope = toponym["boundedBy"]["Envelope"]
    lower_corner = tuple(map(float, envelope["lowerCorner"].split()))
    upper_corner = tuple(map(float, envelope["upperCorner"].split()))
    delta_x = abs(lower_corner[0] - upper_corner[0])
    delta_y = abs(lower_corner[1] - upper_corner[1])
    return delta_x, delta_y


def get_image(toponym_point, delta=(0.05, 0.05), par_l="map"):
    map_params = {
        "ll": f"{toponym_point[0]},{toponym_point[1]}",
        "spn": f"{delta[0]},{delta[1]}",
        "l": par_l,
        "pt": f"{toponym_point[0]},{toponym_point[1]},round"
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print(response, response.reason, response.url, end='\n')
        return
    Image.open(BytesIO(response.content)).show()


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    toponym = get_toponym(toponym_to_find)
    point = get_point(toponym)
    spn = get_spn(toponym)
    get_image(toponym_point=point, delta=spn)


if __name__ == '__main__':
    main()
