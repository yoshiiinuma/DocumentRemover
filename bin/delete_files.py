"""
Deletes Files in DELETE Folder from Google Drive
"""
#pylint: disable=wrong-import-position,import-error
import argparse
from os.path import dirname, abspath, exists
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from src.archive import Archive

def get_argparser():
    """
    Build Argument Parser
    """
    parser = argparse.ArgumentParser(description='path to env file')
    parser.add_argument('envfile', help='env file path')
    parser.add_argument('adate', nargs='?', help='date that moves data to DELETE folder (YYYYMMDD)')
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
    archive = Archive(args.envfile)
    rslt = archive.delete_folder(args.adate)
    if rslt:
        print('DELETE_FILE Completed')
    else:
        print('DELETE_FILE Failed')

if __name__ == '__main__':
    main()
