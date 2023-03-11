import os

import requests
import pygame
import sys


def main():
    ll = 'll=37.038186,55.312148'
    http = 'https://static-maps.yandex.ru/1.x/?'
    par_l = 'l=map'
    par_z = 'z=7'
    pt1 = 'pt=37.558212,55.789704~37.43525,55.818103~37.557843,55.71909'
    map_request = f'{http}{ll}&{par_z}&{par_l}&{pt1}'
    response = requests.get(map_request)
    if not response:
        print(response.status_code)
        sys.exit(1)
    screen = pygame.display.set_mode((600, 450))
    map_file = 'map.png'
    with open(map_file, 'wb') as f:
        f.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    main()
