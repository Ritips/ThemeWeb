import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--count", action="store_true")
parser.add_argument("--num", action="store_true")
parser.add_argument("--sort", action="store_true")
parser.add_argument("f", type=str)


if __name__ == '__main__':
    args = parser.parse_args()
    if not args.f:
        print('ERROR')
        exit()
    try:
        with open(args.f, 'r', encoding='utf-8') as f_read:
            data = list(map(str.strip, f_read.readlines()))
            if args.sort:
                data = sorted(data)
            if args.num:
                for i, el in enumerate(data):
                    print(i, el)
            else:
                for el in data:
                    print(el)
            if args.count:
                print(f'rows count: {len(data)}')
    except FileNotFoundError:
        print('ERROR')
        exit()
