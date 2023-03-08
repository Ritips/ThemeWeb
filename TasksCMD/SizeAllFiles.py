import os


def human_read_format(size, count=0):
    values = ['Б', 'КБ', 'МБ', 'ГБ']
    if size >= 1024 and count < 3:
        count += 1
        size = round(size / 1024)
    if size >= 1024 and count < 3:
        return human_read_format(size, count)
    return f'{size}{values[count]}'


def get_files_sizes():
    output = ''
    for root, dirs, files in os.walk('.'):
        for filename in files:
            try:
                output += f'{filename} {human_read_format(os.path.getsize(filename))} \n'
            except FileNotFoundError:
                pass
    return output


if __name__ == '__main__':
    print(get_files_sizes())
