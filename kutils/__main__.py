"""
CL interaction with kutils as a script
"""

from pathlib import Path
import argparse
from kutils import Configuration
import json

cfg_file_name = 'localconf'


def run():
    """
    Main runner for kutils via CLI.

    utilizes argparse
    """
    parser = argparse.ArgumentParser(prog='kutils', description='Execute a kutils task')
    parser.add_argument('-e', '--execute-type', type=str, choices=['youtube', 'twitter'],
                        help='choose to run either "twitter" or "youtube" to check either links')
    parser.add_argument('-s', '--setup-file-location', type=str,
                        help='specify the location of the configuration JSON file')
    parser.add_argument('-mo', '--num-months', type=int,
                        help='specify the number of months to determine Twitter inactivity for fansites (default = 12)')
    args = parser.parse_args()
    print(args)
    '''
    parse args
    if -s arg is not there and we havent been 
    '''


def test():
    conf = Configuration()



if __name__ == "__main__":
    run()
    # test()
