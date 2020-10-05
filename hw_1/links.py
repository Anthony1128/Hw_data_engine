import os
import hashlib

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
                # print(f'{file_path} is a duplicate of {originfile}')
                os.remove(file_path)
                os.link(originfile, file_path)
            else:
                files_hash[filehash] = file_path
    return files_hash

# hard_link(input_path)






