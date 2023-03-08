import sys


check_args = sys.argv[1:]
f_sort = False
out = {}


for el in check_args:
    if el == '--sort':
        f_sort = True
    elif '=' in el and len(el.split('=')) == 2:
        key, value = el.split('=')[0], el.split('=')[-1]
        out[key] = value


if f_sort:
    for key in sorted(out):
        print(f'Key: {key} Value: {out[key]}')
else:
    for key in out:
        print(f'Key: {key} Value: {out[key]}')
