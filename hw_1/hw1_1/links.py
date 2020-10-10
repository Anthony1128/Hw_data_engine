import os
import sys
import hashlib
import argparse

# input_path = os.getcwd()
# print(input_path)


def hard_link(input_path):
    # collect all files and directories 
    walk = os.walk(input_path)
    # stores hash of file as key and path of file as value
    files_hash = {}

    for dirpath, dirnames, filenames in walk:
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            with open(file_path, 'rb') as file:
                content = file.read()
            filehash = hashlib.md5(content).hexdigest()
            if filehash in files_hash.keys():
                originfile = files_hash[filehash]
                os.remove(file_path)
                os.link(originfile, file_path)
            else:
                files_hash[filehash] = file_path
    return files_hash


def main(input_path):
    hard_link(input_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='transform duplicate of a file '
                                    'to a hard link in given directory')
    args = parser.parse_args()
    main(args.dir)



