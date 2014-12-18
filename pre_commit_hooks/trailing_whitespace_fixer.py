from __future__ import print_function

import argparse
import sys
from plumbum import local

from pre_commit_hooks.util import entry


@entry
def fix_trailing_whitespace(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to fix')
    args = parser.parse_args(argv)

    bad_whitespace_files = local['grep'][
        ('-l', '[[:space:]]$') + tuple(args.filenames)
    ](retcode=None).strip().splitlines()

    if bad_whitespace_files:
        print('Trailing Whitespace detected in: {0}'.format(', '.join(bad_whitespace_files)))

        print('psst, you can fix this by running')
        print("    set -i '' -e s/[[:space:]]*$//", ' '.join(map(repr, bad_whitespace_files)))
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(fix_trailing_whitespace())
