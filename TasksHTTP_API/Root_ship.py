import requests
import pygame
import os


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


def get_image(toponym_coords, spn="0,0.2", l1="map", pl=None):
    map_request = "https://static-maps.yandex.ru/1.x/?ll=" + toponym_coords + f"&spn={spn}&l={l1}"
    if pl:
        map_request = map_request + f'&pl={",".join(pl)}'
    map_response = requests.get(map_request)
    if not map_response:
        print(map_response.reason, map_response)
        print(map_response.url)
        return
    map_file = 'map.png'
    with open(map_file, 'wb') as f_image:
        f_image.write(map_response.content)
    image = pygame.image.load(map_file)
    os.remove(map_file)
    return image


def main():
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption('Root')
    point_0 = get_point("бульв. Головнина")
    point_1 = get_point("Петергоф")
    point_2 = get_point("Зенит Петербург")
    point_3 = get_point('Дворцовая пристань')
    point_4 = get_point("Сенатская пристань")
    point_5 = get_point("причал Набережная Лейтенанта Шмидта")
    point_6 = get_point("Санкт-Петербург Галерный остров")
    points = [point_1, point_2, point_3, point_4, point_5, point_6, point_1]
    print(points)
    image = get_image(point_0, pl=points)
    if not image:
        print('No image')
        return
    screen.blit(image, (0, 0))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        pygame.display.flip()


if __name__ == '__main__':
    main()
