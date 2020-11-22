from random import randint
import os
import gzip


# creates random bin files with random content
def bin_files_create(input_folder):
    for i in range(10):
        content = b''
        zero = b'\x00'
        one = b'\x01'
        l = [zero, one]
        for j in range(randint(20, 100)):
            content += l[randint(0, 1)]
        with gzip.open(f'{input_folder}/file{i}.bin.gz', 'wb') as f:
            f.write(content)


def clear_folder(folder):
    directory = os.path.abspath(folder)
    files = os.listdir(directory)
    for file in files:
        if 'file' in file:
            os.remove(f'{directory}/{file}')


if __name__ == '__main__':
    bin_files_create('input')
    # clear_folder('input')







