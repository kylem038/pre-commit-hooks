import os
import subprocess
import sys

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
    os.rename(path_of_new_merge, new_path)
    return new_path


def check_for_django_migrations(argv=None):
    output = subprocess.check_output(
        get_env_python() + ' manage.py makemigrations --merge  --noinput',
        shell=True)

    if 'No conflicts detected to merge' in output:
        return 0
    elif 'Created new merge migration ' in output:
        new_path = rename_merge_file(output)
        print 'Created new merge migration', new_path
        print 'Please add and commit it'
        return 1
    else:
        print 'Your migrations look like they could use a merge.'
        print 'psst, you can probably fix this by running'
        print '    ./manage.py makemigrations --merge'
        print "    (give it a weird name so it doesn't conflict when somebody else does this.)"
        print "Rather than 0012_merge.py, how about '0012_{}_merge.py'?".format(identifier())
        return 1

if __name__ == '__main__':
    sys.exit(check_for_django_migrations())
