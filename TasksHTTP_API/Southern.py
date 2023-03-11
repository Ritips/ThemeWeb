import requests


def get_point(name):
    geocoder_api = 'https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b'
    geocode = f"&geocode={name}&format=json"
    request = geocoder_api + geocode
    response = requests.get(request)
    if not response:
        print(response.reason, response)
        print(response.url)
        return
    json_object = response.json()
    toponym = json_object["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    return ','.join(toponym["Point"]["pos"].split())


def main():
    cities = input().split(',')
    p1, p2, p3 = map(lambda x: get_point(x), cities)
    n = max((p1, p2, p3))
    if p1 == n:
        print(cities[0])
    elif p2 == n:
        print(cities[1])
    else:
        print(cities[-1])


if __name__ == '__main__':
    main()


# Дербент,Москва,Санкт-Петербург -- Дербент,Певек,Лонгйир
