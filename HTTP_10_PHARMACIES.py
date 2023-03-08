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


def find_places(text='аптека', lang='ru_RU', ll=None, kind='biz', amount=10):
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
        "type": kind,
        "results": amount
    }
    response = requests.get(search_api_server, params=search_params)
    if not response:
        print(response.reason, response, response.url, end='\n')
        return
    json_object = response.json()
    sp = []
    for organization in json_object["features"]:
        org_name = organization["properties"]["CompanyMetaData"]["name"]
        org_address = organization["properties"]["CompanyMetaData"]["address"]
        point = organization["geometry"]["coordinates"]
        org_time = organization["properties"]["CompanyMetaData"]["Hours"]["text"]
        sp.append((org_name, org_address, point, org_time))
    return sp


def get_point(toponym):
    return tuple(map(float, toponym["Point"]["pos"].split()))


def get_image(toponym_point, delta=(0.05, 0.05), par_l="map", pt=None):
    pt = f"{toponym_point[0]},{toponym_point[1]},round" if not pt else pt
    map_params = {
        "ll": f"{toponym_point[0]},{toponym_point[1]}",
        "spn": f"{delta[0]},{delta[1]}",
        "l": par_l,
        "pt": pt
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    if not response:
        print(response, response.reason)
        print(response.url)
        return
    Image.open(BytesIO(response.content)).show()


def get_spn_list_coords(sp_coords):
    max_x = max(sp_coords, key=lambda x: x[0])[0]
    max_y = max(sp_coords, key=lambda x: x[1])[1]
    min_x = min(sp_coords, key=lambda x: x[0])[0]
    min_y = min(sp_coords, key=lambda x: x[1])[1]
    return max_x - min_x, max_y - min_y


def create_marks(places):
    pt = []
    for place in places:
        p, org_time = place[-2], place[-1]
        if org_time:
            if 'круглосуточно' in org_time:
                pt.append(f'{p[0]},{p[1]},pm2dgm')
            else:
                pt.append(f'{p[0]},{p[1]},pm2dbm')
        else:
            pt.append(f'{p[0]},{p[1]},pm2grm')
    return '~'.join(pt)


def main():
    address = ' '.join(sys.argv[1:])
    current_toponym = get_toponym(address)
    current_point = get_point(current_toponym)
    str_ll = f"{current_point[0]},{current_point[1]}"
    places = find_places(ll=str_ll)
    points = list(map(lambda x: x[-2], places))
    points.append(list(current_point))
    pt = create_marks(places)
    spn = get_spn_list_coords(points)
    get_image(points[0], pt=pt, delta=spn)


if __name__ == '__main__':
    main()
