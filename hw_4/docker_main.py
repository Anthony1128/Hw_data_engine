import os
import docker
import math
import json
import logging


def get_filenames(directory):
    filenames_in_dir = os.listdir(directory)
    return sorted([filename for filename in filenames_in_dir
                   if filename.endswith('.gz')])


def reduce_results(results):
    reduce_result_dict = {list(i.keys())[0]: 0 for i in results}
    for result in results:
        for filename, count in result.items():
            reduce_result_dict[filename] += count
    return reduce_result_dict


class MRframework:
    def __init__(self, input_dir='input', n=3):
        self.image_name = 'hw4_mr'
        self.input_directory = os.path.abspath(input_dir)
        self.output_directory = os.path.abspath('output')
        self.N = n

        self.reduce_results = reduce_results
        self.get_filenames = get_filenames

        self.client = docker.APIClient()
        logging.basicConfig(format='%(levelname)s:%(message)s',
                            level=logging.INFO)

    def container_run(self, files):
        logging.info("Launching container for {}".format(", ".join(files)))

        host_config = self.client.create_host_config(
            binds={
                self.input_directory: {
                    'bind': '/input',
                    'mode': 'ro'
                },
                self.output_directory: {
                    'bind': '/output',
                    'mode': 'rw'
                }
            },
            )

        environment = {
                'INPUT_FILENAMES': ';'.join(files)
            }

        container = self.client.create_container(
            image=self.image_name,
            user=os.getuid(),
            host_config=host_config,
            environment=environment)

        self.client.start(container)

        return container

    def reduce_output_files(self):
        filenames = [filename for filename in os.listdir(self.output_directory)
                     if filename.endswith('.json')]
        results = []
        for filename in filenames:
            with open(os.path.join(self.output_directory,
                                   filename), 'r') as output_file:
                results.append(json.loads(output_file.read()))
        return self.reduce_results(results)

    def run(self):
        filenames = self.get_filenames(self.input_directory)
        chunk_size = int(math.ceil(len(filenames) / float(self.N)))
        containers = []

        for i in range(0, len(filenames), chunk_size):
            files_chunk = filenames[i:i + chunk_size]
            containers.append(self.container_run(files_chunk))

        logging.info("Waiting for containers to finish...")

        for container in containers:
            exit_code = self.client.wait(container)
            logging.info("Container exited with code {}".format(exit_code))

        script_results = self.reduce_output_files()
        logging.info("Script results{}".format(script_results))
        return script_results






