import os
import subprocess
import sys
import argparse

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


def rename_merge_file(output):
    pwd = os.getcwd() + '/'
    loc = output.find('Created new merge migration ')
    path_start = output.find(pwd, loc)
    next_newline = output.find('\n', path_start)
    path_of_new_merge = output[path_start:next_newline]
    new_path = rreplace(path_of_new_merge, 'merge.py', identifier() + '_merge.py')
    return 'mv {} {}'.format(path_of_new_merge, new_path)


def check_for_django_migrations(argv=None):
    output = subprocess.check_output(
        get_env_python() + ' manage.py makemigrations --merge  --noinput --dry-run',
        shell=True)
    if 'No conflicts detected to merge' not in output:
        print 'Your migrations look like they could use a merge.'
        print 'psst, you can probably fix this by running'
        print '    ./manage.py makemigrations --merge && {}'.format(rename_merge_file(output))
        return 1

    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check')
    args = parser.parse_args(argv)
    for arg in args:
        print args


if __name__ == '__main__':
    sys.exit(check_for_django_migrations())
