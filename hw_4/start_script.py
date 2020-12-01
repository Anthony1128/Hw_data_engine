import argparse
from docker_main import MRframework


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', help='path to directory with .gz files')
    parser.add_argument('N', help='Number of mappers')
    args = parser.parse_args()

    mr_fr = MRframework(args.dir, args.N)
    return mr_fr.run()


if __name__ == '__main__':
    main()
