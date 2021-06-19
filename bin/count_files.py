"""
Counts test files on Google Drive
"""
#pylint: disable=wrong-import-position,import-error
import argparse
from os.path import dirname, abspath, exists
import sys
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import src.config as Config
from src.drive import Drive

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
    conf = Config.load(args.envfile)
    client = Drive(conf)
    client.connect()
    cnt = 0
    token = ''
    for fid in client.src_folder_ids():
        query = f"'{fid}' in parents"
        while True:
            rslt = client.list(query, 200, token)
            cnt += len(rslt['files'])
            token = rslt.get('nextPageToken')
            if not token:
                break
            print(cnt)
    client.close()
    print(f'{cnt} Files Found')

if __name__ == '__main__':
    main()
