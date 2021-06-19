"""
Sets 1 to Requests.Archived
"""
#pylint: disable=wrong-import-position,import-error
import argparse
from os.path import dirname, abspath, exists
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from src.archive import Archive

#pylint: disable=duplicate-code
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
    rslt = archive.set_archive_flag_to_requests()
    print(f'{int(rslt/2)} Requests Archived')
    print(f'{int(rslt/2)} ArchivedRequests Updated')

if __name__ == '__main__':
    main()
