import requests


def get_metro_by_point(coord):
    if len(coord.split()) < 2:
        print("Coords aren't separated by space or amount of arguments less than two")
        return
    if len(coord.split()) > 3:
        print("Too many arguments")
        return
    coords = ",".join(coord.split())
    api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
    geocoder_api = 'https://geocode-maps.yandex.ru/1.x/?'
    geocoder_params = {
        "apikey": api_key,
        "geocode": f"{coords}",
        "ll": coords,
        "format": "json",
        "kind": "metro"
    }
    response = requests.get(geocoder_api, params=geocoder_params)
    if not response:
        print(response, response.reason, response.url)
        return
    json_object = response.json()
    toponym = json_object["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    name_metro = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
    return name_metro


def main():
    coords = input("Input coordinates separated by space: ")
    print(get_metro_by_point(coords))


if __name__ == '__main__':  # 30.234805 59.94839
    main()
