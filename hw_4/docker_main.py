import os
import docker
import math
import json
import logging


# collect file names of only gzip files
def get_filenames(directory):
    filenames_in_dir = os.listdir(directory)
    return sorted([filename for filename in filenames_in_dir
                   if filename.endswith('.gz')])


# combine all output files (result of map tasks) in one dictionary
def reduce_results(results):
    reduce_result_dict = {list(i.keys())[0]: 0 for i in results}
    for result in results:
        for filename, count in result.items():
            reduce_result_dict[filename] += count
    return reduce_result_dict


class MRframework:
    def __init__(self, input_dir='input', n=3):
        self.image_name = 'hw_4'
        self.input_directory = os.path.abspath(input_dir)
        self.output_directory = os.path.abspath('output')
        self.N = n

        self.reduce_results = reduce_results
        self.get_filenames = get_filenames

        self.client = docker.APIClient()
        logging.basicConfig(format='%(levelname)s:%(message)s',
                            level=logging.INFO)

    # build an image according to Dockerfile
    def image_build(self):
        container_limits = {
            'memory': '1g'
        }
        return self.client.build(path='./', tag=self.image_name,
                                 encoding='utf-8',
                                 container_limits=container_limits)

    # runs a single container based on the previous image
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

    # collects all the output files result in one list
    def reduce_output_files(self):
        filenames = [filename for filename in os.listdir(self.output_directory)
                     if filename.endswith('.json')]
        results = []
        for filename in filenames:
            with open(os.path.join(self.output_directory,
                                   filename), 'r') as output_file:
                results.append(json.loads(output_file.read()))
        return self.reduce_results(results)

    # Entrypoint
    def run(self):
        filenames = self.get_filenames(self.input_directory)

        # amount of files for each container
        chunk_size = int(math.ceil(len(filenames) / float(self.N)))
        containers = []

        # building an image
        image = self.image_build()
        for id_i, step in enumerate(image):
            logging.info(f'Build Image: Step {id_i}')

        # split input files by even chunks and start containers
        for i in range(0, len(filenames), chunk_size):
            files_chunk = filenames[i:i + chunk_size]
            containers.append(self.container_run(files_chunk))

        logging.info("Waiting for containers to finish...")

        # waits for containers to finish and removes them
        for container in containers:
            exit_code = self.client.wait(container)
            logging.info("Container exited with code {}".format(exit_code))
            self.client.remove_container(container['Id'])

        # reduce task
        script_results = self.reduce_output_files()
        logging.info("Script results{}".format(script_results))

        return script_results






