import argparse

parser = argparse.ArgumentParser()
parser.add_argument("values", nargs='*', type=str)


def calculator3dot0(values):
    if len(values) == 0:
        return 'NO PARAMS'
    if len(values) == 1:
        return 'TOO FEW PARAMS'
    if len(values) == 2:
        try:
            val1, val2 = int(values[0]), int(values[1])
            return val1 + val2
        except Exception as er:
            return ''.join([s for s in str(er.__class__).split()[-1] if s.lower() in 'qwertyuiopasdfghjklzxcvbnm'])
    return 'TOO MANY PARAMS'


if __name__ == '__main__':
    args = parser.parse_args()
    print(calculator3dot0(args.values))
