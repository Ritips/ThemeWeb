import argparse


parser = argparse.ArgumentParser()
parser.add_argument("arg", nargs=3)
args = parser.parse_args()

if args.arg:
    for el in args.arg:
        print(el)
else:
    print('no args')
