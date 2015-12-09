from fabric.api import env, task, sudo, cd, run, local, prefix, lcd, get, execute, settings
from fabric.context_managers import quiet
from fabric.contrib.project import rsync_project
from fabric.contrib.files import sed
from datetime import datetime
import os
from os.path import basename, dirname


env.key_filename = "../../ec2.pem"
env.hosts = ["ec2-52-16-175-249.eu-west-1.compute.amazonaws.com"]
env.user = "ubuntu"
virtual_env_name = "elcid-rfh"


@task
def deploy():
    changes = local("git status --porcelain", capture=True)
    if len(changes):
        print "you have uncommited changes {}".format(changes)
    else:
        git_branch_name = local('git rev-parse --abbrev-ref HEAD', capture=True)
        with prefix(". /usr/share/virtualenvwrapper/virtualenvwrapper.sh"):
            with prefix("workon {}".format(virtual_env_name)):
                run("git pull origin {}".format(git_branch_name))
                run("pip install -r requirements.txt")
                run("python manage.py migrate")
                run("python manage.py collectstatic --noinput")
                run("pkill supervisord; pkill gunicorn")
                run("supervisord -c etc/production.conf")
