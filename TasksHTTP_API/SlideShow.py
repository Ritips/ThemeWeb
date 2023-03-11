import pygame
import requests
import os


def get_point(name):
    if not name:
        return
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


def show(images):
    screen = pygame.display.set_mode((600, 450))
    pygame.display.set_caption("SlideShow")
    running = True
    index = 0
    screen.blit(images[index], (0, 0))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                index = (index + 1) % len(images)
                screen.blit(images[index], (0, 0))
        pygame.display.flip()


def main():
    headers = input('Введите названия/адреса мест через "; "').split('; ')
    images = [get_image(get_point(header)) for header in headers]
    show(images)


if __name__ == '__main__':
    main()
