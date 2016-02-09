from fabric.api import env, task, local, lcd
import os


env.hosts = ["elcid-uch-test.openhealthcare.org.uk"]
env.user = "ubuntu"
project_name = "elcid"

def get_requirements():
    """
    looks for a requirements file in the same directory as the
    fabfile. Parses it,
    """
    fabfile_dir = os.path.realpath(os.path.dirname(__file__))

    with lcd(fabfile_dir):
        requirements = local("less requirements.txt", capture=True).split("\n")
        package_to_version = {}

        for requirement in requirements:
            s = requirement.split("===")
            package_to_version[s[0]] = s[1]

    return package_to_version

def pass_github_urls(some_url):
    """
    takes in something that looks like a git hub url in a fabfile e.g.
    -e git+https://github.com/openhealthcare/opal-referral.git@v0.1.2#egg=opal_referral
    returns opal-referral
    """
    if "github" in some_url:
        package_name = some_url.split("@")[0].split("/")[-1]
        version = some_url.split("@")[-1].split("/")[-1]



@task
def checkout_current_environment():
    """
    looks for a requirements file in the same directory as the
    fabfile. Parses it,
    """
    fabfile_dir = os.path.realpath(os.path.dirname(__file__))

    with lcd(fabfile_dir):
        requirements = local("less requirements.txt", capture=True).split("\n")
        package_to_version = {}

        for requirement in requirements:
            s = requirement.split("===")
            package_to_version[s[0]] = s[1]
