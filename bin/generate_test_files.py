"""
Generates test files on Google Drive
"""
#pylint: disable=wrong-import-position,import-error,R0801
import argparse
from os.path import dirname, abspath, exists
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import src.config as Config
import src.drive_file_generator as Generator

def get_argparser():
    """
    Build Argument Parser
    """
    parser = argparse.ArgumentParser(description='path to env file')
    parser.add_argument('envfile', help='env file path')
    parser.add_argument('limit', nargs='?', default=1000, type=int, help='data size limit for db query')
    parser.add_argument('offset', nargs='?', default=0, type=int, help='record offset for db query')
    parser.add_argument('max', nargs='?', default=10000, type=int, help='total number of records to handle')
    return parser

def main():
    """
    Main Function
    """
    args = get_argparser().parse_args()
    if exists(args.envfile):
        print('ENV File Found: ' + args.envfile)
    else:
        print('ENV File Not Found: ' + args.envfile)
    print(args)
    conf = Config.load(args.envfile)
    Generator.generate(conf, args.limit, args.offset, args.max)

if __name__ == '__main__':
    main()
