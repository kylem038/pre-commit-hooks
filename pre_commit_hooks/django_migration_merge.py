import os
import subprocess
import sys
import argparse
import re

from .identifiers import identifier


def get_env_python():
    """
    I'm not proud of this hack, but I do believe it was necessary.
    """
    line = subprocess.check_output(
        "< .git/hooks/pre-commit grep 'ENV_PYTHON='",
        shell=True).splitlines()[0]
    return line.split('=')[-1].strip("'")


def rreplace(s, old, new, occurrences=1):
    li = s.rsplit(old, occurrences)
    return new.join(li)


def parse_output_and_suggest_rename(output):
    pwd = os.getcwd() + '/'
    loc = output.find('Created new merge migration ')
    path_start = output.find(pwd, loc)
    next_newline = output.find('\n', path_start)
    path_of_new_merge = output[path_start:next_newline].replace(pwd + '/', '')
    new_path = rreplace(path_of_new_merge, 'merge.py', identifier() + '_merge.py')
    os.remove(path_of_new_merge)
    return 'mv {} {}'.format(path_of_new_merge, new_path)


def rename_merge_file(current_name):
    new_path = rreplace(current_name, 'merge.py', identifier() + '_merge.py')
    return 'mv {} {}'.format(current_name, new_path)


MERGE_MIGRATION = re.compile(r'\w+/migrations/\d\d\d\d_merge\.py')


def check_for_django_migrations(argv=None):
    output = subprocess.check_output(
        get_env_python() + ' manage.py makemigrations --merge  --noinput',
        shell=True)
    if 'No conflicts detected to merge' not in output:
        print 'Your migrations look like they could use a merge.'
        print 'psst, you can probably fix this by running'
        print '    ./manage.py makemigrations --merge && {}'.format(
            parse_output_and_suggest_rename(output))
        return 1

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)
    needs_renaming = [fname for fname in args.filenames if MERGE_MIGRATION.match(fname)]
    if needs_renaming:
        print 'Some merge migrations need renaming.'
        print 'Consider running:'
        print '    ', ' && '.join(rename_merge_file(n) for n in needs_renaming)
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(check_for_django_migrations())
