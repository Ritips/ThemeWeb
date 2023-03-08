import sys


if len(sys.argv) > 1:
    alpha = 'qwertyuiopasdfghjklzxcvbnm'
    res = 0
    for i in range(len(sys.argv[1:])):
        try:
            if not i % 2:
                res += int(sys.argv[i + 1])
            else:
                res -= int(sys.argv[i + 1])
        except Exception as er:
            out = ''.join([symbol for symbol in str(er.__class__).split()[-1] if symbol.lower() in alpha])
            print(out)
            exit()
    print(res)
else:
    print('NO PARAMS')
