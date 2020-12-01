import gzip
from use_case import clear_folder
from docker_main import MRframework


def bin_file_create(input_folder, zeros, ones, i):
    content = b''
    zero = b'\x00'
    one = b'\x01'
    for j in range(zeros):
        content += zero
    for j in range(ones):
        content += one
    with gzip.open(f'{input_folder}/file{i}.bin.gz', 'wb') as f:
        f.write(content)


def test_use_case():
    bin_file_create('input', 10, 3, 0)
    bin_file_create('input', 24, 7, 1)
    bin_file_create('input', 101, 14, 2)
    mr_fr = MRframework()
    assert mr_fr.run() == {'file0.bin.gz': 3, 'file1.bin.gz': 7, 'file2.bin.gz': 14}
    clear_folder('input')
    clear_folder('output')











