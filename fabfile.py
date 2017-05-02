from fabric.api import env, task, local, lcd, run, prefix
from fabric.operations import prompt
from fabric.context_managers import warn_only
import os


env.hosts = ["elcid-uch-test.openhealthcare.org.uk"]
env.user = "ubuntu"
project_name = "elcid"
virtual_env_name = "elcid"
fabfile_dir = os.path.realpath(os.path.dirname(__file__))


def check_for_uncommitted():
    changes = local("git status --porcelain", capture=True)
    return len(changes)


def get_requirements():
    """
    looks for a requirements file in the same directory as the
    fabfile. Parses it,
    """

    with lcd(fabfile_dir):
        requirements = local("less requirements.txt", capture=True).split("\n")

        package_to_version = {}

        for requirement in requirements:
            parsed_url = parse_github_urls(requirement)

            if parsed_url:
                package_to_version.update(parsed_url)

    return package_to_version


def parse_github_urls(some_url):
    """
    takes in something that looks like a git hub url in a fabfile e.g.
    -e git+https://github.com/openhealthcare/opal-referral.git@v0.1.2#egg=opal_referral
    returns opal-referral
    """

    if "github" in some_url and "opal" in some_url:
        package_name = some_url.split("@")[0].split("/")[-1]
        package_name = package_name.replace(".git", "")
        version = some_url.split("@")[-1].split("#")[0]
        return {package_name: version}


def checkout(package_name_version):
    with lcd(fabfile_dir):
        with lcd(".."):
            existing_packages = local("ls", capture=True).split("\n")
            uncommitted = []

            for package_name, version in package_name_version.iteritems():
                if package_name in existing_packages:
                    with lcd(package_name):
                        if check_for_uncommitted():
                            uncommitted.append(package_name)

            if len(uncommitted):
                print "we have uncommited changes in {} quitting".format(
                    ", ".join(uncommitted)
                )
                return

            for package_name, version in package_name_version.iteritems():
                if not version:
                    print "found NO VERSION for {} using master".format(
                        package_name
                    )
                    version = "master"
                print "looking at {}".format(package_name)

                if package_name not in existing_packages:
                    print "cloning {}".format(package_name)
                    local("git clone {}".format(package_name))
                    with lcd(package_name):
                        print "checking out {0} to {1}".format(
                            package_name, version
                        )
                else:
                    with lcd(package_name):
                        local("git fetch")

                with lcd(package_name):
                    local("git checkout {}".format(version))
                    local("git pull origin {}".format(version))
                    local("python setup.py develop")


def db_commands(username):
    cmds =  [
        "python manage.py migrate",
        "python manage.py loaddata data/elcid.teams.json",
        "python manage.py load_lookup_lists -f data/lookuplists/lookuplists.json",
        'echo "from opal.models import Role; Role.objects.create(name=\'micro_haem\')" | python ./manage.py shell',
        "python manage.py create_random_data"
    ]
    python_cmd = "echo '"
    python_cmd += "from django.contrib.auth.models import User; "
    python_cmd += "User.objects.create_superuser(\"{0}\", \"{0}@example.com\", \"{0}1\")".format(username)
    python_cmd += "' | python ./manage.py shell"
    cmds.append(python_cmd)
    return cmds

def push_to_heroku(remote_name):
    with lcd(fabfile_dir):
        current_branch_name = local(
            "git rev-parse --abbrev-ref HEAD", capture=True
        )
        local("git push {0} {1}:master".format(
            remote_name, current_branch_name)
        )


@task
def create_heroku_instance(name, username):
    """
    creates and populates a heroku instance
    TODO make sure that we're fully committed git wise before pushing
    """
    with lcd(fabfile_dir):
        local("heroku apps:create {}".format(name))
        git_url = "https://git.heroku.com/{}.git".format(name)
        local("git remote add {0} {1}".format(name, git_url))
        push_to_heroku(name)
        with warn_only():
            # heroku somtimes has memory issues doing migrate
            # it seems to work fine if we just migrate opal first
            # it will later fail because content types haven't
            # been migrated, but that's fine we'll do that later
            local("heroku run --app {0} python manage.py migrate opal".format(
                name
            ))
        for db_command in db_commands(username):
            local("heroku run --app {0} {1}".format(name, db_command))


@task
def production_deploy():
    # TODO include the supervisor commands
    # synch the nginx conf
    with lcd(fabfile_dir):
        local("python manage.py migrate")
        local("python manage.py collectstatic --noinput")


@task
def checkout_project():
    checkout(get_requirements())


@task
def create_db(username):
    with lcd(fabfile_dir):
        with warn_only():
            # heroku somtimes has memory issues doing migrate
            # it seems to work fine if we just migrate opal first
            # it will later fail because content types haven't
            # been migrated, but that's fine we'll do that later
            local("python manage.py migrate opal")

        for db_command in db_commands(username):
            local(db_command)

@task
def deploy(key_file_name="../ec2.pem"):
    env.key_filename = key_file_name
    changes = local("git status --porcelain", capture=True)
    if len(changes):
        print " {}".format(changes)
        proceed = prompt(
            "you have uncommited changes, do you want to proceed",
            default=False,
            validate=bool
        )

        if not proceed:
            return


    git_branch_name = local('git rev-parse --abbrev-ref HEAD', capture=True)
    with prefix(". /usr/share/virtualenvwrapper/virtualenvwrapper.sh"):
        with prefix("workon {}".format(virtual_env_name)):
            run("git fetch")
            run("git checkout {}".format(git_branch_name))
            run("git pull origin {}".format(git_branch_name))
            run("pip install -r requirements.txt")
            run("python manage.py migrate")
            run("python manage.py collectstatic --noinput")
            run("supervisorctl -c etc/test.conf restart gunicorn")
            run("supervisorctl -c etc/test.conf restart celery")


@task
def restart_all(key_file_name="../ec2.pem"):
    env.key_filename = key_file_name
    with prefix(". /usr/share/virtualenvwrapper/virtualenvwrapper.sh"):
        with prefix("workon {}".format(virtual_env_name)):
            run("supervisorctl -c etc/test.conf restart gunicorn")
            run("supervisorctl -c etc/test.conf restart celery")
            run("supervisorctl -c etc/test.conf restart gloss")
            run("supervisorctl -c etc/test.conf restart gloss_flask")
