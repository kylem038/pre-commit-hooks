from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import sys
import platform

from pre_commit_hooks.util import entry

quote_file = repr # wrap with quotes

def file_ends_with_newline(file_obj):
    # Test for newline at end of file
    # Empty files will throw IOError here
    try:
        file_obj.seek(-1, os.SEEK_END)
    except IOError:
        return True
    last_character = file_obj.read(1)
    # last_character will be '' for an empty file
    if last_character != b'\n' and last_character != b'':
        return False
    return True

def file_ends_with_multiple_newlines(file_obj):
    try:
        file_obj.seek(-2, os.SEEK_END)
    except IOError:
        return False
    last_two_chars = file_obj.read(2)
    if last_two_chars == b'\n\n':
        return True
    return False

FIX_MISSING_NEWLINE = '''sed -i '' -e s/[[:space:]]*$// {files}'''
FIX_MULTIPLE_NEWLINES = r'''for ff in {files}; do sed -i '' -e :a -e '/^\n*$/{{$d;N;ba' -e '}}' $ff; done'''

if platform.system() != 'Darwin':
    FIX_MISSING_NEWLINE = FIX_MISSING_NEWLINE.replace("-i ''", "-i")
    FIX_MULTIPLE_NEWLINES = FIX_MULTIPLE_NEWLINES.replace("-i ''", "-i")

@entry
def end_of_file_checker(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)

    multiple_newline_files = []
    missing_newline_files = []
    for filename in args.filenames:
        # Read as binary so we can read byte-by-byte
        with open(filename, 'rb+') as file_obj:
            if not file_ends_with_newline(file_obj):
                missing_newline_files.append(filename)
            if file_ends_with_multiple_newlines(file_obj):
                multiple_newline_files.append(filename)
    if missing_newline_files:
        print("These files are missing a newline at the end:", ", ".join(missing_newline_files))
        print("You can fix this with the following:")
        print("    ", FIX_MISSING_NEWLINE.format(files=' '.join(map(quote_file, missing_newline_files))))
        print()
    if multiple_newline_files:
        print("These files have extra newlines at the end:", ", ".join(multiple_newline_files))
        print("You can fix this with the following:")
        print("    ", FIX_MULTIPLE_NEWLINES.format(files=' '.join(map(quote_file, multiple_newline_files))))
        print()

    return 1 if missing_newline_files or multiple_newline_files else 0


if __name__ == '__main__':
    sys.exit(end_of_file_checker())
