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
    parser.add_argument('archive_date', help='date that files are moved to DELETE folder (YYYYMMDD)')
    parser.add_argument('current_date', nargs='?', help='date that files are deleted (YYYYMMDD)')
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
    rslt = archive.delete_folder(args.archive_date, args.current_date)
    if rslt:
        print('DELETE_FILE Completed')
    else:
        print('DELETE_FILE Failed')

if __name__ == '__main__':
    main()
