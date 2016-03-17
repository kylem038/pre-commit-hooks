import random
import subprocess
import sys

with open('animals', 'r') as f:
    animals = [line.strip() for line in f]
with open('adjectives', 'r') as f:
    adjectives = [line.strip() for line in f]


def identifier():
    return '{}_{}'.format(random.choice(adjectives), random.choice(animals))


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
        print "    (give it a weird name so it doesn't conflict when somebody else does this.)"
        print "Rather than 0012_merge.py, how about '0012_{}_merge.py'?".format(identifier())
        return 1

if __name__ == '__main__':
    sys.exit(check_for_django_migrations())
