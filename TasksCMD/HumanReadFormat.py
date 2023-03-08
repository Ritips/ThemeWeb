def human_read_format(size, count=0):
    values = ['Б', 'КБ', 'МБ', 'ГБ']
    if size >= 1024 and count < 3:
        count += 1
        size = round(size / 1024)
    if size >= 1024 and count < 3:
        return human_read_format(size, count)
    return f'{size}{values[count]}'


if __name__ == '__main__':
    print(human_read_format(1073741824))
