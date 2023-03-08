import zipfile
import time
import os


def make_reserve_arc(source, dest, name_file='zip_archive'):
    if not source or not dest:
        print('No source or no dest --> exit')
        return
    name_file = 'zip_archive' if not name_file else name_file
    name_file = name_file.replace('.zip', '')
    name_file = f'{name_file} {time.strftime("%H-%M-%S")}.zip'
    if not os.path.exists(dest):
        os.mkdir(dest)
    dest = f'{dest}/{name_file}'
    with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED, True) as z_file:
        for current_dir, dirs, files in os.walk(source):
            for file in files:
                z_file.write(os.path.join(current_dir, file))


def main():
    dir_source, dir_dest, zip_name = input('Input dir_source: '), input('Input dir_dest: '), input('Input zip name: ')
    try:
        make_reserve_arc(dir_source, dir_dest, zip_name)
    except FileNotFoundError:
        print('FileNotFoundError')
        main()


if __name__ == '__main__':
    main()
