import requests


def get_info(start=None, geocode=None, f_out='json'):
    response = requests.get(f'{start}&geocode={geocode}&format={f_out}')

    if response:
        json_object = response.json()
        toponym = json_object["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return toponym["metaDataProperty"]["GeocoderMetaData"]["Address"]["postal_code"]
    return None


def main():
    begin = "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b"
    geocode1 = "Петровки, 38"
    print(get_info(start=begin, geocode=geocode1))


if __name__ == '__main__':
    main()
