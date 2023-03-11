import requests
from distance import lonlat_distance
from io import BytesIO
from PIL import Image
import sys


def find_place(text='аптека', lang='ru_RU', ll=None, kind='biz'):
    if not ll:
        print(f'Missing argument: ll: {ll}')
        return
    search_api_server = "https://search-maps.yandex.ru/v1/"
    api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
    search_params = {
        "apikey": api_key,
        "text": text,
        "lang": lang,
        "ll": ll,
        "type": kind
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print(response.reason, response, response.url, end='\n')
        return
    json_object = response.json()
    organization = json_object["features"][0]
    org_name = organization["properties"]["CompanyMetaData"]["name"]
    org_address = organization["properties"]["CompanyMetaData"]["address"]
    point = organization["geometry"]["coordinates"]
    org_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
    current_point = tuple(map(float, ll[0].split(',')))
    return org_name, org_address, org_time, lonlat_distance(current_point, point), point


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
        print(response, response.reason)
        print(response.url)
        return
    Image.open(BytesIO(response.content)).show()


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


def get_spn(toponym):
    envelope = toponym["boundedBy"]["Envelope"]
    lower_corner = tuple(map(float, envelope["lowerCorner"].split()))
    upper_corner = tuple(map(float, envelope["upperCorner"].split()))
    delta_x = abs(lower_corner[0] - upper_corner[0])
    delta_y = abs(lower_corner[1] - upper_corner[1])
    return delta_x, delta_y


def main():
    address_ll = sys.argv[1:]
    metadata = find_place(ll=address_ll)
    toponym = get_toponym(f"{metadata[-1][0]},{metadata[-1][1]}")
    spn = get_spn(toponym)
    get_image(metadata[-1], delta=spn)
    for el in metadata[:-1]:
        print(el, end='\n')


if __name__ == '__main__':
    main()
