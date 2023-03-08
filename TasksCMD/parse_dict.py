import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--sort", action="store_true")
parser.add_argument("arg", type=str, nargs="*")


if __name__ == '__main__':
    args = parser.parse_args()
    out = {}
    for el in args.arg:
        if '=' in el and len(el.split('=')) == 2:
            key, val = el.split('=')[0], el.split('=')[-1]
            out[key] = val

    if args.sort:
        for key in sorted(out):
            print(f'Key: {key} Value: {out[key]}')
    else:
        for key in out:
            print(f'Key: {key} Value: {out[key]}')
