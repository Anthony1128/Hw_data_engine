import os
import gzip
import json

INPUT_DIRECTORY = '/input'
OUTPUT_DIRECTORY = '/output'


def map_binary(filename, input_folder):
    count = 0
    with gzip.open(f'{input_folder}/{filename}', 'rb') as input_file:
        content = input_file.read()
        for bit in content:
            if bit == 1:
                count += 1
    return {filename: count}


def listdir_nohidden(path):
    for file in os.listdir(path):
        if not file.startswith('.'):
            yield file


if __name__ == '__main__':
    input_filenames = os.environ['INPUT_FILENAMES'].split(';')
    for input_filename in input_filenames:
        output_filename = f'{input_filename[:5]}.json'
        map_result = map_binary(input_filename, INPUT_DIRECTORY)
        with open(os.path.join(OUTPUT_DIRECTORY,
                               output_filename), 'w') as output_file:
            output_file.write(json.dumps(map_result))










