import os
import hashlib
import argparse
import asyncio


# stores hash of a file as key and path of file as value
files_hash = {}
# stores state checks of a file
state_checks = {}


# searching for duplicates and transform them into hard links
async def hard_link(dirpath, dirnames, filenames):
    global files_hash
    global state_checks
    for filename in filenames:
        file_path = os.path.join(dirpath, filename)
        stat = list(os.stat(file_path))
        id = stat[1]

        with open(file_path, 'rb') as file:
            content = file.read()
        filehash = hashlib.md5(content).hexdigest()

        if filehash in files_hash.keys():
            # check if it is already hard link
            if id == files_hash[filehash][1]:
                state_checks[file_path] = 'is already a hard link'
                continue

            originfile = files_hash[filehash][0]
            os.remove(file_path)
            os.link(originfile, file_path)
            state_checks[file_path] = 'was a duplicate. now a hard link'
        else:
            files_hash[filehash] = [file_path, id]
            state_checks[file_path] = 'is origin'
    return files_hash


async def main():
    # getting argument
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='transform duplicate of a file '
                                    'to a hard link in given directory')
    args = parser.parse_args()

    # collect all files and directories
    walk = os.walk(args.dir)

    result = [await hard_link(dirpath, dirnames, filenames) for dirpath, dirnames, filenames in walk]


if __name__ == '__main__':
    asyncio.run(main())



