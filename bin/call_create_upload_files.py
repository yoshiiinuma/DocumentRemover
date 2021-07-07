"""
Create UploadedFiles table
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
    conf = Config.load(args.envfile)
    Generator.call_create_upload_files(conf)

if __name__ == '__main__':
    main()
