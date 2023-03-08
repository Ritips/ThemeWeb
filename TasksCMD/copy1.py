import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--upper", action="store_true")
parser.add_argument("--lines", type=int)
parser.add_argument("source", type=str)
parser.add_argument("dest", type=str)


if __name__ == '__main__':
    args = parser.parse_args()
    with open(args.source, 'r', encoding='utf-8') as f_read:
        data = list(f_read.readlines())
        if args.upper:
            data = list(map(str.upper, data))
        with open(args.dest, 'w', encoding='utf-8') as f_write:
            for string in data[:args.lines]:
                print(string, file=f_write, end='')

