import os


def human_read_format(size, count=0):
    values = ['Б', 'КБ', 'МБ', 'ГБ']
    if size >= 1024 and count < 3:
        count += 1
        size = round(size / 1024)
    if size >= 1024 and count < 3:
        return human_read_format(size, count)
    return f'{size}{values[count]}'


def get_top_ten_vip_things_to_delete(path):
    ten_sizes = {}
    for current_dir, dirs, files in os.walk(path):
        for file in files:
            size = os.path.getsize(f'{current_dir}/{file}')
            if len(ten_sizes) < 10:
                ten_sizes[size] = file
            elif size > min(ten_sizes):
                del ten_sizes[min(ten_sizes)]
                ten_sizes[size] = file
    max_length = len(ten_sizes[max(ten_sizes, key=lambda x: len(ten_sizes[x]))])

    for key in ten_sizes:
        print(f'{ten_sizes[key]}{" " * (max_length - len(ten_sizes[key]))} - {human_read_format(key)}')


if __name__ == '__main__':
    get_top_ten_vip_things_to_delete(input())
