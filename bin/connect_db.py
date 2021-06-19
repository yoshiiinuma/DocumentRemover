"""
Check access to the database
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
    parser.add_argument('envfile', nargs='?', default='.env', help='env file path')
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
    conf = Config.load(args.envfile)
    db = DB(conf)
    rslt = db.connect()
    if rslt:
        print(rslt)
        print('Connection Establised Successfully!')
        #rslt = db.ping()
        #print(rslt)
    else:
        print('Cannot Connect')
        db.show_errors()
    db.close()

if __name__ == '__main__':
    main()
