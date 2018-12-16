from __future__ import print_function
from __future__ import unicode_literals

import argparse
import re

def check_file_for_db_url(filenames):
    bad_files = []

    for filename in filenames:
        with open(filename, 'r') as content:
            text_body = content.read()
            match1 = re.search('Server=localhost;UID=', text_body)
            if match1 is not None:
                # naively match the entire file, low chance of incorrect collision
                bad_files.append(filename)

    return bad_files

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to run')
    args = parser.parse_args(argv)

    bad_filenames = check_file_for_db_url(args.filenames)
    if bad_filenames:
        for bad_file in bad_filenames:
            print('SQL Server URL found: {0}'.format(bad_file))
        return 1
    else:
        return 0

if __name__ == '__main__':
    exit(main())
