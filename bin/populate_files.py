"""
Populates ArchiveFiles with information from Google Drive
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
    total = 0
    limit = 200
    while True:
        cnt = archive.populate_file_info(limit)
        if cnt == 0:
            break
        total += cnt
        print(f'POPULATE_FILE_INFO: CUR {cnt} / TOTAL {total} ArchivedFiles Populated')
    print(f'POPULATE_FILE_INFO: {total} ArchivedFiles Populated')

if __name__ == '__main__':
    main()
