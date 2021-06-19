"""
Generates test data
"""
#pylint: disable=wrong-import-position,import-error
import argparse
from datetime import datetime
from os.path import dirname, abspath, exists
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import src.config as Config
import src.db_data_generator as Generator

def get_argparser():
    """
    Build Argument Parser
    """
    parser = argparse.ArgumentParser(description='path to env file')
    parser.add_argument('envfile', help='env file path')
    parser.add_argument('owner', help='owner of data')
    parser.add_argument('date', help='start date (yyyymmdd)')
    parser.add_argument('days', nargs='?', default=5, type=int, help='the number of days')
    parser.add_argument('quantity', nargs='?', default=1, type=int,
                        help='the number of requests per day')
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
    base_date = datetime.strptime(args.date, '%Y%m%d')
    #data = Generator.bulk_generate_requests(args.owner, base_date)
    #data = Generator.bulk_generate_travelers(args.owner, base_date)
    #data = Generator.bulk_generate_documents(args.owner, base_date)
    #for r in data:
    #    print(r)
    #data = Generator.bulk_generate(args.owner, base_date, args.num_of_reqs)
    #for r in data['requests']:
    #    print(r)
    #for r in data['travelers']:
    #    print(r)
    #for r in data['documents']:
    #    print(r)
    Generator.populate(conf, args.owner, base_date, args.days, args.quantity)


if __name__ == '__main__':
    main()
