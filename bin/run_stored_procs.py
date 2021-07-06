"""
Run Stored Procedures
"""
#pylint: disable=wrong-import-position,import-error,invalid-name
import argparse
import re
from datetime import datetime
from os.path import dirname, abspath, exists
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import src.config as Config
from src.db import DB

def check_date(value):
    if not re.match(r'^20\d{6}$', value):
        raise argparse.ArgumentTypeError('Current Date must be YYYYMMDD: ' + value)
    return re.sub(r'^(20\d{2})(\d{2})(\d{2})$', r'\1-\2-\3', value)

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
    parser.add_argument('current_date', type=check_date, help='assumed to be the current date (YYYYMMDD)')
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
    db = DB(conf)
    db.connect()
    rslt = db.exec(f"CALL CreateArchiveRequests({args.days1}, '{args.current_date}')")
    print('CreateArchiveRequests Called')
    print(f'{rslt} ArchivedRequests Created')
    rslt = db.exec(f"CALL CreateArchiveRequestsWithInvalidDate({args.days2}, '{args.current_date}')")
    print('CreateArchiveRequestsWithInvalidDate Called')
    print(f'{rslt} ArchivedRequests With Invalid Date Created')
    rslt = db.exec('CALL CreateArchiveFiles()')
    print(f'{rslt} ArchivedFiles Created')
    db.close()

if __name__ == '__main__':
    main()
