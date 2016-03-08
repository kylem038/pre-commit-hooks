import subprocess
import sys


def get_env_python():
    """
    I'm not proud of this hack, but I do believe it was necessary.
    """
    line = subprocess.check_output(
        "< .git/hooks/pre-commit grep 'ENV_PYTHON='",
        shell=True).splitlines()[0]
    return line.split('=')[-1].strip("'")


def check_for_django_migrations(argv=None):
    output = subprocess.check_output(
        get_env_python() + ' manage.py makemigrations --merge  --noinput --dry-run',
        shell=True)
    if 'No conflicts detected to merge' in output:
        return 0
    else:
        print 'Your migrations look like they could use a merge.'
        print 'psst, you can probably fix this by running'
        print '    ./manage.py makemigrations --merge'
        return 1

if __name__ == '__main__':
    sys.exit(check_for_django_migrations())
