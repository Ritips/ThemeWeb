import requests


def get_info(start=None, geocode=None, f_out="json"):
    response = requests.get(f'{start}&geocode={geocode}&format={f_out}')

    federal_districts = []
    if response:
        json_object = response.json()
        toponym = json_object["response"]["GeoObjectCollection"]["featureMember"]
        for geo_dict in toponym:
            search = geo_dict["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]
            for key in search:
                if 'область' in key["name"].lower() and key["name"] not in federal_districts:
                    federal_districts.append(key["name"])
        return '; '.join(federal_districts)
    return None


def main():
    begin = "https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b"
    geocode1 = "Барнаул"
    geocode2 = "Мелеуз"
    geocode3 = "Йошкар-Ола"
    geocodes = [geocode1, geocode2, geocode3]
    spaces = len(max(geocodes, key=len))

    for el in geocodes:
        print(f"City: {el}{' ' * (spaces - len(el))}\tdistricts: {get_info(start=begin, geocode=el)}")


if __name__ == '__main__':
    main()
