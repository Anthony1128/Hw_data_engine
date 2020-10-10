import os
import shutil
from random import randint
from links import hard_link


def create_case():
    cur_dir = os.getcwd()
    test_path = cur_dir + '/test'
    os.mkdir(test_path)

    # creating three different files
    for i in range(3):
        with open(test_path + f'/file{i}', 'w') as f:
            f.write(f'file{i}')

    # creating random amount of directories and copies of files in them
    for i in range(randint(1, 5)):
        os.mkdir(test_path + f'/dir{i}')
        for j in range(randint(1, 5)):
            shutil.copyfile(test_path + '/file0', test_path + f'/dir{i}/file0_{j}')
        for j in range(randint(1, 5)):
            shutil.copyfile(test_path + '/file1', test_path + f'/dir{i}/file1_{j}')
        for j in range(randint(1, 5)):
            shutil.copyfile(test_path + '/file2', test_path + f'/dir{i}/file2_{j}')

    return test_path


# deleting tested folder with its content
def clear_case():
    cur_dir = os.getcwd()
    test_path = cur_dir + '/test'
    shutil.rmtree(test_path)


# collecting stat (id and links) of all files
def check_stat(input_path):
    walk = os.walk(input_path)
    files_stat = {}
    for dirpath, dirnames, filenames in walk:
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            stat = list(os.stat(file_path))
            files_stat[filename] = {
                'id': stat[1],
                'links': stat[3]
            }
    return files_stat


def test_case():
    test_path = create_case()
    hard_link(test_path)
    file_stat = check_stat(test_path)
    for filename in file_stat.keys():
        if 'file0' in filename:
            assert file_stat['file0']['id'] == file_stat[filename]['id']
            assert file_stat['file0']['links'] == file_stat[filename]['links']
        if 'file1' in filename:
            assert file_stat['file1']['id'] == file_stat[filename]['id']
            assert file_stat['file1']['links'] == file_stat[filename]['links']
        if 'file2' in filename:
            assert file_stat['file2']['id'] == file_stat[filename]['id']
            assert file_stat['file2']['links'] == file_stat[filename]['links']
    clear_case()
