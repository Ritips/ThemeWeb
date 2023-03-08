import json
import pygame
import requests
import random
import os

cities = ['Москва', 'Санкт-Петербург', 'Екатиринбург', 'Казань', 'Самара', 'Новосибирск', 'Пермь', 'Нижний Новгород',
          'Владивосток', 'Краснодар', 'Челябинск', 'Воронеж', 'Тюмень', 'Волгоград', 'Саратов', 'Владимир', 'Рязань',
          'Ростов-на-Дону', 'Калининград', 'Красноярск', 'Ульяновск', 'Ярославль', 'Сочи', 'Иваново', 'Иркутск',
          'Астрахань', 'Великий Новгород', 'Петрозаводск', 'Томск', 'Оренбург', 'Мурманск', 'Ставрополь',
          'Махачкала', 'Кострома', 'Уфа', 'Смоленск', 'Йошкар-Ола', 'Ижевск', 'Киров']
dictionary = {}


def create_json_file_cities():
    global dictionary
    global cities
    if not os.path.exists('cities.json'):
        for city in cities:
            dictionary[city] = get_toponym(city)
        with open('cities.json', 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, ensure_ascii=False, indent=2)
    else:
        with open('cities.json', encoding='utf-8') as f:
            dictionary = json.load(f)
        cities.clear()
        for key in dictionary:
            cities.append(key)


def get_point(city):
    return tuple(map(float, dictionary[city]["Point"]["pos"].split()))


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
    map_file = 'map_file.png'
    with open(map_file, 'wb') as f:
        f.write(response.content)
    image = pygame.image.load(map_file)
    os.remove(map_file)
    return image


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


def start_game():
    screen = pygame.display.set_mode((600, 450))
    pygame.display.set_caption("Click to change image")
    while True:
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                screen.fill("black")
                city = random.choice(cities)
                point = get_point(city)
                par_l = random.choice(("map", "sat"))
                delta = (30, 30)
                screen.blit(get_image(point, par_l=par_l, delta=delta), (0, 0))
                pygame.display.flip()


def main():
    create_json_file_cities()
    start_game()


if __name__ == '__main__':
    main()
