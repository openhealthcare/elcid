from fabric.api import env, task, run, local, prefix
from fabric.operations import prompt


env.hosts = ["elcid-uch-test.openhealthcare.org.uk"]
env.user = "ubuntu"
virtual_env_name = "elcid"


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
            run("pkill supervisord; pkill gunicorn")
            run("supervisord -c etc/production.conf")
