import zipfile


def search(zip_name):
    for el in zip_name.namelist():
        spaces = el.count('/')
        if '.' in el:
            print(f'{" " * 2 * spaces}{el.split("/")[-1]}')
        else:
            print(f'{" " * 2 * (spaces - 1)}{el.split("/")[-2]}')


search(zipfile.ZipFile('input.zip', 'r'))
