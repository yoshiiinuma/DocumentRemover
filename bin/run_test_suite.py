"""
Runs test suite
"""
#pylint: disable=wrong-import-position,import-error
import argparse
from datetime import datetime
from os.path import dirname, abspath, exists
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))
from src.test_suite_runner import TestSuiteRunner

def get_argparser():
    """
    Build Argument Parser
    """
    parser = argparse.ArgumentParser(description='path to env file')
    parser.add_argument('envfile', help='env file path')
    parser.add_argument('date', help='start date (yyyymmdd)')
    parser.add_argument('days', type=int, help='the number of days to run test')
    parser.add_argument('retention1', type=int,
                        help='retention period for regular requests until archive')
    parser.add_argument('retention2', type=int,
                        help='retention period for irregular requests until archive')
    parser.add_argument('retention3', type=int,
                        help='retention period until delete')
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
    runner = TestSuiteRunner(args.envfile, args.retention1, args.retention2, args.retention3)
    runner.run(args.date, args.days)

if __name__ == '__main__':
    main()
