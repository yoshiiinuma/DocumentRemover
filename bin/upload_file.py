"""
Generates upload files on Google Drive
"""
#pylint: disable-msg=R0801
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
    parser.add_argument('uploadfile', help='file path to upload')
    return parser

FILES = (
    './assets/FileDeleted.png',
    './assets/FileArchived.png',
    './assets/Sample.docx',
    './assets/Sample.jpg',
    './assets/Sample.pdf',
    './assets/Sample.png'
)

def main():
    """
    Main Function
    """
    args = get_argparser().parse_args()
    if exists(args.envfile):
        print('ENV File Found: ' + args.envfile)
    else:
        print('ENV File Not Found: ' + args.envfile)
    if exists(args.uploadfile):
        print('UPLOAD File Found: ' + args.uploadfile)
    else:
        print('UPLOAD File Not Found: ' + args.uploadfile)
    conf = Config.load(args.envfile)
    client = Drive(conf)
    client.connect()
    #for fpath in FILES:
    #    r = client.create_file(fpath, conf['DRIVE_APP_ROOT'])
    #    print(r)
    rslt = client.create_file(args.uploadfile, conf['DRIVE_APP_ROOT'])
    print(rslt)
    client.close()

if __name__ == '__main__':
    main()
