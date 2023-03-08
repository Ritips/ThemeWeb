import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--file", type=str)


def count_lines(name_file):
    try:
        with open(name_file, 'r', encoding='utf-8') as f_read:
            return len(list(map(str.strip, f_read.readlines())))
    except FileNotFoundError:
        return 0


if __name__ == '__main__':
    args = parser.parse_args()
    print(count_lines(args.file))
