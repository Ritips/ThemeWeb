import zipfile


def search(zip_name):
    for el in zip_name.namelist():
        spaces = el.count('/')
        info = zip_name.getinfo(el)
        if not info.is_dir():
            file_volume = human_read_format(zip_name.getinfo(el).file_size)
            file_volume = f' {file_volume}' if file_volume else ''
            print(f'{" " * 2 * spaces}{el.split("/")[-1]}{file_volume}')
        else:
            print(f'{" " * 2 * (spaces - 1)}{el.split("/")[-2]}')


def human_read_format(size, count=0):
    values = ['Б', 'КБ', 'МБ', 'ГБ']
    if size >= 1024 and count < 3:
        count += 1
        size = round(size / 1024)
    if size >= 1024 and count < 3:
        return human_read_format(size, count)
    return f'{size}{values[count]}'


with zipfile.ZipFile('input.zip') as z_file:
    search(z_file)
