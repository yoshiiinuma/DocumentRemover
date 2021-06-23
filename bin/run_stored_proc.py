"""
Run Stored Procedures
"""
#pylint: disable=wrong-import-position,import-error,invalid-name
import argparse
from os.path import dirname, abspath, exists
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import src.config as Config
from src.db import DB

def get_argparser():
    """
    Build Argument Parser
    """
    parser = argparse.ArgumentParser(description='path to env file')
    parser.add_argument('envfile', help='env file path')
    parser.add_argument('days1', default=60, type=int,
                        help='retention period for regular requests until archive')
    parser.add_argument('days2', default=240, type=int,
                        help='retention period for irregular requests until archive')
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
    db = DB(conf)
    db.connect()
    rslt = db.exec(f'CALL CreateArchiveRequests({args.days1})')
    print('CreateArchiveRequests Called')
    print(f'{rslt} ArchivedRequests Created')
    rslt = db.exec(f'CALL CreateArchiveRequestsWithInvalidDate({args.days2})')
    print('CreateArchiveRequestsWithInvalidDate Called')
    print(f'{rslt} ArchivedRequests With Invalid Date Created')
    rslt = db.exec('CALL CreateArchiveFiles()')
    print(f'{rslt} ArchivedFiles Created')
    db.close()

if __name__ == '__main__':
    main()
