import os
import docker
import math
import json

CONTAINER_NAME = 'hw4_mr'
INPUT_DIRECTORY = os.path.abspath('input')
OUTPUT_DIRECTORY = os.path.abspath('output')
N = 3

client = docker.APIClient()


def get_filenames(directory):
    filenames_in_dir = os.listdir(directory)
    return sorted([filename for filename in filenames_in_dir
                   if filename.endswith('.gz')])


def container_run(files):
    print("Launching container for {}".format(", ".join(files)))

    host_config = client.create_host_config(
        binds={
            INPUT_DIRECTORY: {
                'bind': '/input',
                'mode': 'ro'
            },
            OUTPUT_DIRECTORY: {
                'bind': '/output',
                'mode': 'rw'
            }
        },
        )

    environment = {
            'INPUT_FILENAMES': ';'.join(files)
        }

    container = client.create_container(
        image=CONTAINER_NAME,
        user=os.getuid(),
        host_config=host_config,
        environment=environment)

    client.start(container)

    return container


def reduce_output_files():
    filenames = [filename for filename in os.listdir(OUTPUT_DIRECTORY)
                 if filename.endswith('.json')]
    results = []
    for filename in filenames:
        with open(os.path.join(OUTPUT_DIRECTORY, filename), 'r') as output_file:
            results.append(json.loads(output_file.read()))
    return reduce_results(results)


def reduce_results(results):
    reduce_result_dict = {list(i.keys())[0]: 0 for i in results}
    for result in results:
        for filename, count in result.items():
            reduce_result_dict[filename] += count
    return reduce_result_dict


if __name__ == '__main__':
    filenames = get_filenames(INPUT_DIRECTORY)
    chunk_size = int(math.ceil(len(filenames)/float(N)))
    containers = []

    for i in range(0, len(filenames), chunk_size):
        files_chunk = filenames[i:i+chunk_size]
        containers.append(container_run(files_chunk))

    print("Waiting for containers to finish...")

    for container in containers:
        exit_code = client.wait(container)
        print("Container exited with code {}".format(exit_code))

    reduced_results = reduce_output_files()
    print(reduced_results)






