import os
import gzip
import json

INPUT_DIRECTORY = '/input'
OUTPUT_DIRECTORY = '/output'


# read file by 1Gb chunks
def read_in_chunks(file_object, chunk_size=10**9):
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


# counts non-zero bits in gzip file
def map_binary(filename, input_folder):
    count = 0
    with gzip.open(f'{input_folder}/{filename}', 'rb') as input_file:
        for chunk in read_in_chunks(input_file):
            for bit in chunk:
                if bit == 1:
                    count += 1
    return {filename: count}


if __name__ == '__main__':
    input_filenames = os.environ['INPUT_FILENAMES'].split(';')
    for input_filename in input_filenames:
        output_filename = f'{input_filename[:-3]}.json'
        map_result = map_binary(input_filename, INPUT_DIRECTORY)

        # writes the map result in output folder as json file
        with open(os.path.join(OUTPUT_DIRECTORY,
                               output_filename), 'w') as output_file:
            output_file.write(json.dumps(map_result))










