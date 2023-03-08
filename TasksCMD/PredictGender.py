import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--barbie", default=50, type=int)
parser.add_argument("--cars", default=50, type=int)
parser.add_argument("--movie", default="other")


def main():
    args = parser.parse_args()
    barbie = args.barbie
    cars = args.cars
    movie = args.movie
    barbie = barbie if 0 <= barbie <= 100 else 50
    cars = cars if 0 <= cars <= 100 else 50
    if movie == "other":
        movie = 50
    elif movie == "football":
        movie = 100
    else:
        movie = 0
    boy = int((100 - barbie + cars + movie) / 3)
    girl = 100 - boy
    print(f'boy: {int(boy)}')
    print(f'girl: {int(girl)}')


if __name__ == "__main__":
    main()
