import sys


f_count = False
f_num = False
f_sort = False
file = None


for el in sys.argv:
    if el == '--num':
        f_num = True
    elif el == '--count':
        f_count = True
    elif el == '--sort':
        f_sort = True
    else:
        file = el


try:
    with open(file, 'r', encoding='utf-8') as f:
        data = list(map(str.strip, f.readlines()))
        if f_sort:
            data = sorted(data)
        if f_num:
            for i, el in enumerate(data):
                print(i, el)
        else:
            for el in data:
                print(el)
        if f_count:
            print(f'rows count: {len(data)}')
except FileNotFoundError:
    print('ERROR')
