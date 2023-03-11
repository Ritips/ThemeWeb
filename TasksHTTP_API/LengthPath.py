import requests
import pygame
from math import sqrt
import os


def get_points():
    # points = input("Input coords(x,y) of points separated by ';': ").split(';')
    points = "29.906775,59.881227;30.211906,59.971947;30.314224," \
             "59.941989;30.300507,59.936616;30.272938,59.93108".split(';')

    p = []
    for point in points:
        if len(point.split(',')) != 2:
            print(f"Incorrect format: {point}. This point was excluded")
            continue
        p.append(tuple(map(lambda x: float(x), ''.join(list(filter(lambda x: x in '0123456789.,', point))).split(','))))
    length_path = sum([sqrt((p[i + 1][0] - p[i][0]) ** 2 + (p[i + 1][1] - p[i][1]) ** 2) for i in range(len(p) - 1)])
    return p, length_path


def get_image(point, points):
    api_server = "https://static-maps.yandex.ru/1.x/?"
    params = {
        "ll": f"{point[0]},{point[1]}",
        "size": "650,450",
        "l": "map",
        "spn": "5,0.02",
        "pl": ",".join([f"{p[0]},{p[1]}" for p in points]),
        "pt": f"{point[0]},{point[1]},pm2rdm"
    }
    response = requests.get(api_server, params=params)
    if not response:
        print(response, response.url, response.reason)
        return
    map_file = 'map.png'
    with open(map_file, 'wb') as f_image:
        f_image.write(response.content)
    image = pygame.image.load(map_file)
    os.remove(map_file)
    show_image(image)


def show_image(image):
    screen = pygame.display.set_mode((600, 450))
    pygame.display.set_caption('Path')
    screen.blit(image, (0, 0))
    while True:
        [exit() for event in pygame.event.get() if event.type == pygame.QUIT]
        pygame.display.flip()


def main():
    points, length_path = get_points()
    print(f"Path's length = {length_path * 122}")
    mid_point = points[len(points) // 2]
    get_image(mid_point, points)


p2 = ['29.906775,59.881227', '30.211906,59.971947', '30.314224,59.941989', '30.300507,59.936616', '30.272938,59.93108',
      '30.270297,59.916884', '29.906775,59.881227']
# 29.906775,59.881227;30.211906,59.971947;30.314224,59.941989;30.300507,59.936616;30.272938,59.93108
if __name__ == '__main__':
    main()
