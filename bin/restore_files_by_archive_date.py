"""
Restores all the files in DELETE Folder of specified date
back to the original location
"""
#pylint: disable=wrong-import-position,import-error
import argparse
import re
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
    parser.add_argument('archive_date', help='date that moves data to DELETE folder (YYYYMMDD)')
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
        return
    if not re.match(r'^20\d{6}$', args.archive_date):
        print('Invalid Archive Date: ' + args.archive_date)
        return
    archive = Archive(args.envfile)
    rslt = archive.restore_files_by_archive_date(args.archive_date)
    if rslt:
        print(f'Files in DELETE_FOLDER/{args.archive_date} Restored')
    else:
        print(f'File Restore for RequestID {args.request_id} Failed')

if __name__ == '__main__':
    main()
