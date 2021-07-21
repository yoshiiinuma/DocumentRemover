"""
Tests drive connection
"""
#pylint: disable=wrong-import-position,import-error,R0801
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
    #parser.add_argument('folder_id', help='folder id to retrieve files')
    parser.add_argument('name', help='file name to retrieve')
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
    client = Drive(conf)
    r = client.connect()
    #r = client.get_files_in_folder(args.folder_id)
    #for f in r['files']:
    #    print(f"name {f['name']} id {f['id']}")
    r = client.get_files_by_name([args.name])
    for f in r:
        print(f)
    client.close()

if __name__ == '__main__':
    main()
