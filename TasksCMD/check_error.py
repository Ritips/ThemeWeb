import argparse


parser = argparse.ArgumentParser()
parser.add_argument("string", type=str)


def print_error(message):
    print(f'ERROR: {message}!!')


if __name__ == "__main__":
    print("Welcome to my program")
    print_error(parser.parse_args().string)
