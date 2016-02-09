from fabric.api import env, task, local, lcd
import os


env.hosts = ["elcid-uch-test.openhealthcare.org.uk"]
env.user = "ubuntu"
project_name = "elcid"
fabfile_dir = os.path.realpath(os.path.dirname(__file__))

def get_requirements():
    """
    looks for a requirements file in the same directory as the
    fabfile. Parses it,
    """

    with lcd(fabfile_dir):
        requirements = local("less requirements.txt", capture=True).split("\n")

        package_to_version = {}

        for requirement in requirements:
            package_to_version.update(pass_github_urls(requirement))

    return package_to_version

def pass_github_urls(some_url):
    """
    takes in something that looks like a git hub url in a fabfile e.g.
    -e git+https://github.com/openhealthcare/opal-referral.git@v0.1.2#egg=opal_referral
    returns opal-referral
    """

    if "github" in some_url and "opal" in some_url:
        package_name = some_url.split("@")[0].split("/")[-1]
        version = some_url.split("@")[-1].split("#")[0]
        return {package_name: version}

@task
def checkout_project(package_name_version):
    with lcd(fabfile_dir):
        with lcd(".."):
            existing_packages = local("ls").split("\n")

            for package_name, version in package_name_version.iteritems():
                if package_name in existing_packages:
                    print "we are going to checkout {}".format(package_name)
                else:
                    print "we are going to clone {}".format(package_name)
