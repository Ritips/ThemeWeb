import os
import sys
import pygame
import requests


def main():
    map_request = f'https://static-maps.yandex.ru/1.x/?ll=149.125531,-35.306907&spn=60,0.02&l=sat'
    response = requests.get(map_request)
    if not response:
        print(response.status_code, response.reason)
        sys.exit(1)
    map_file = 'map.png'
    with open(map_file, 'wb') as f:
        f.write(response.content)

    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()

    os.remove(map_file)


if __name__ == '__main__':
    main()
