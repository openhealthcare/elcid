""" A wise man once said, is there any point in testing
    files where you're just calling system calls and everything is mocked.

    And he was wise.

    We think there probably is, just to reassure one of their pythonic
    assumptions.

    Obviously its not as good as running it for realsies
"""
import json
import tempfile
import os
import sys
import mock
import datetime
from opal.core.test import OpalTestCase

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import fabfile
from fabfile import Env


class FakeFabricCapture(object):
    def __init__(self, some_str, stdout=None, stderr=None, failed=None):
        self.some_str = some_str
        self.stdout = stdout or some_str
        self.stderr = stderr
        self.failed = failed

    def __str__(self):
        return self.some_str


@mock.patch("fabfile.local")
@mock.patch("fabfile.os")
@mock.patch("fabfile.print", create=True)
class CloneBranchTestCase(OpalTestCase):
    def test_clone_branch(self, print_statement, os, local):
        os.path.isdir.return_value = False
        branch_name = "some-branch"
        expected = "git clone -b some-branch \
https://github.com/openhealthcare/elcid \
/usr/local/ohc/elcid-some-branch"
        fabfile.clone_branch(branch_name)
        print_statement.assert_called_once_with(
            'Cloning into /usr/local/ohc/elcid-some-branch'
        )
        local.assert_called_once_with(expected)

    def test_clone_branch_raises(self, print_statement, os, local):
        os.path.isdir.return_value = True
        branch_name = "some-branch"
        with self.assertRaises(ValueError) as err:
            fabfile.clone_branch(branch_name)
        self.assertEqual(
            str(err.exception),
            "/usr/local/ohc/elcid-some-branch already exists"
        )


@mock.patch("fabfile.json")
@mock.patch("fabfile.os")
class CreatePrivateSettingsTestCase(OpalTestCase):
    def test_create_private_settings(self, os, json):
        m = mock.mock_open()
        os.path.isfile.return_value = False
        fab_open = "fabfile.open"
        with mock.patch(fab_open, m, create=True):
            fabfile.create_private_settings()
        called = json.dump.call_args[0][0]
        self.assertEqual(
            called,
            dict(
                db_password="",
                host_string="",
                additional_settings={},
                remote_password=""
            )
        )
        m.assert_called_once_with('/usr/local/ohc/private_settings.json', 'w')

    def test_private_settings_already_exist(self, os, json):
        # mock open just in case, we don't want to
        # accidentally write anything
        os.path.isfile.return_value = True
        er = "private settings already exist at \
/usr/local/ohc/private_settings.json"
        with self.assertRaises(ValueError) as err:
            fabfile.create_private_settings()
        self.assertEqual(
            str(err.exception), er
        )


class FabfileTestCase(OpalTestCase):
    def setUp(self):
        # prod env raises an error if any part of the environment already
        # exists
        self.prod_env = fabfile.Env("some_branch", False)
        # test env deletes the existing environment
        self.test_env = fabfile.Env("some_branch", True)


class EnvTestCase(FabfileTestCase):
    def test_project_directory(self):
        self.assertEqual(
            self.prod_env.project_directory,
            "/usr/local/ohc/elcid-some_branch"
        )

    def test_remove_existing(self):
        self.assertFalse(self.prod_env.remove_existing)
        self.assertTrue(self.test_env.remove_existing)

    @mock.patch("fabfile.datetime")
    def test_remote_backup_name(self, dt):
        dt.datetime.now.return_value = datetime.datetime(2017, 9, 21)
        self.assertEqual(
            self.prod_env.remote_backup_name,
            "/usr/local/ohc/var/live/back.21.09.2017.00.00.elcid_some_branch.sql.tar.gz"
        )

    def test_release_name(self):
        self.assertEqual(
            self.prod_env.release_name,
            "elcid-some_branch"
        )

    def test_virtual_env_path(self):
        self.assertEqual(
            self.prod_env.virtual_env_path,
            "/home/ohc/.virtualenvs/elcid-some_branch"
        )

    def test_database_name(self):
        self.assertEqual(
            self.prod_env.database_name,
            "elcid_some_branch"
        )

    @mock.patch("fabfile.datetime")
    def test_backup_name(self, dt):
        dt.datetime.now.return_value = datetime.datetime(
            2017, 9, 7, 11, 12
        )
        self.assertEqual(
            self.prod_env.backup_name,
            "/usr/local/ohc/var/back.07.09.2017.11.12.elcid_some_branch.sql"
        )
        self.assertTrue(dt.datetime.now.called)


@mock.patch('fabfile.os')
class InferCurrentBranchTestCase(FabfileTestCase):
    def test_infer_current_branch_success(self, os):
        os.path.abspath.return_value = "/usr/local/ohc/elcid-something"
        self.assertEqual(
            fabfile.infer_current_branch(),
            "something"
        )

    def test_infer_current_branch_error(self, os):
        os.path.abspath.return_value = "/usr/local/ohc/blah"
        with self.assertRaises(ValueError) as er:
            fabfile.infer_current_branch(),

        expected = "we are in /usr/local/ohc/blah but expect to be in a \
directory beginning with /usr/local/ohc/elcid-"
        self.assertEqual(str(er.exception), expected)


@mock.patch("fabfile.local")
@mock.patch("fabfile.lcd")
@mock.patch("fabfile.print", create=True)
class RunManagementCommandTestCase(FabfileTestCase):
    def test_run_management_command(self, print_statement, lcd, local):
        local.return_value = FakeFabricCapture("something")
        result = fabfile.run_management_command("some_command", self.prod_env)
        local.called_once_with("as")
        self.assertEqual(result, local.return_value)
        lcd.assert_called_once_with("/usr/local/ohc/elcid-some_branch")


@mock.patch("fabfile.print", create=True)
@mock.patch("fabfile.local")
class PipTestCase(FabfileTestCase):

    @mock.patch("fabfile.os")
    def test_pip_prod_create_virtual_env(self, os, local, print_statment):
        os.path.isdir.return_value = True
        with self.assertRaises(ValueError) as er:
            fabfile.pip_create_virtual_env(self.prod_env)

        os.path.isdir.assert_called_once_with(
            "/home/ohc/.virtualenvs/elcid-some_branch"
        )
        self.assertEqual(
            str(er.exception),
            "Directory /home/ohc/.virtualenvs/elcid-some_branch already \
exists"
        )

    def test_pip_test_create_virtual_env_with_remove(
        self, local, print_statement
    ):
        fabfile.pip_create_virtual_env(self.test_env)
        print_statement.assert_called_once_with("Creating new environment")
        first_call = local.call_args_list[0][0][0]
        self.assertEqual(
            first_call,
            "rm -rf /home/ohc/.virtualenvs/elcid-some_branch"
        )
        second_call = local.call_args_list[1][0][0]
        self.assertEqual(
            second_call,
            "virtualenv /home/ohc/.virtualenvs/elcid-some_branch"
        )

    def test_pip_test_create_virtual_env_without_remove(
        self, local, print_statement
    ):
        fabfile.pip_create_virtual_env(self.prod_env)
        local.assert_called_once_with(
            "virtualenv /home/ohc/.virtualenvs/elcid-some_branch"
        )

    def test_pip_install_requirements(self, local, print_statement):
        fabfile.pip_install_requirements(self.prod_env)
        first_call = local.call_args_list[0][0][0]
        self.assertEqual(
            first_call,
            "/home/ohc/.virtualenvs/elcid-some_branch/bin/pip install \
pip==9.0.1"
        )
        second_call = local.call_args_list[1][0][0]
        self.assertEqual(
            second_call,
            "/home/ohc/.virtualenvs/elcid-some_branch/bin/pip install \
setuptools==38.4.0"
        )

        third_call = local.call_args_list[2][0][0]
        self.assertEqual(
            third_call,
            "/home/ohc/.virtualenvs/elcid-some_branch/bin/pip install \
distribute==0.7.3"
        )

        fourth_call = local.call_args_list[3][0][0]

        self.assertEqual(
            fourth_call,
            "/home/ohc/.virtualenvs/elcid-some_branch/bin/pip install -r \
requirements.txt"
        )

    def test_set_project_directory(self, local, print_statement):
        fabfile.pip_set_project_directory(self.prod_env)
        local.assert_called_once_with(
            "echo '/usr/local/ohc/elcid-some_branch' > \
/home/ohc/.virtualenvs/elcid-some_branch/.project"
        )


@mock.patch("fabfile.print", create=True)
@mock.patch("fabfile.local")
class PostgresTestCase(FabfileTestCase):
    def test_postgres_on_prod_raises(self, local, print_function):
        local.return_value = FakeFabricCapture(
            "1", stdout="1", stderr="no problem"
        )
        with self.assertRaises(ValueError) as err:
            fabfile.postgres_create_database(self.prod_env)
        first_call = print_function.call_args_list[0][0][0]
        self.assertEqual(
            first_call,
            "Creating the database"
        )

        second_call = print_function.call_args_list[1][0][0]
        self.assertEqual(
            second_call,
            "no problem"
        )

        third_call = print_function.call_args_list[2][0][0]
        self.assertEqual(
            third_call,
            "1"
        )
        self.assertEqual(
            str(err.exception),
            "database elcid_some_branch already exists"
        )

    def test_progres_create_database_with_test_database_found(
        self, local, print_function
    ):
        local.return_value = FakeFabricCapture("1")
        fabfile.postgres_create_database(self.test_env)
        call_args = local.call_args_list
        self.assertEqual(len(call_args), 4)
        self.assertEqual(
            call_args[0][0][0],
            'sudo -u postgres psql -tAc "SELECT 1 FROM pg_database WHERE \
datname=\'elcid_some_branch\'"'
        )

        self.assertEqual(
            call_args[1][0][0],
            'sudo -u postgres psql --command "DROP DATABASE \
elcid_some_branch"'
        )

        self.assertEqual(
            call_args[2][0][0],
            'sudo -u postgres psql --command "CREATE DATABASE \
elcid_some_branch"'
        )

        self.assertEqual(
            call_args[3][0][0],
            'sudo -u postgres psql --command "GRANT ALL PRIVILEGES ON \
DATABASE elcid_some_branch TO ohc"'
        )

    def test_progres_create_database_without_drop(
        self, local, print_function
    ):
        local.return_value = FakeFabricCapture("0")
        fabfile.postgres_create_database(self.prod_env)
        call_args = local.call_args_list

        self.assertEqual(len(call_args), 3)
        self.assertEqual(
            call_args[0][0][0],
            'sudo -u postgres psql -tAc "SELECT 1 FROM pg_database \
WHERE datname=\'elcid_some_branch\'"'
        )

        self.assertEqual(
            call_args[1][0][0],
            'sudo -u postgres psql --command "CREATE DATABASE \
elcid_some_branch"'
        )

        self.assertEqual(
            call_args[2][0][0],
            'sudo -u postgres psql --command "GRANT ALL PRIVILEGES ON \
DATABASE elcid_some_branch TO ohc"'
        )

    @mock.patch('fabfile.os')
    def test_postgres_load_database_if_exists(
        self, os, local, print_function
    ):
        os.path.isfile.return_value = True
        fabfile.postgres_load_database("some_backup_full_path", self.prod_env)
        local.assert_called_once_with(
            "sudo -u postgres psql -d elcid_some_branch -f \
some_backup_full_path"
        )
        print_function.assert_called_once_with(
            "Loading the database elcid_some_branch"
        )


@mock.patch("fabfile.print", create=True)
class ServicesTestCase(FabfileTestCase):
    @mock.patch('fabfile.os')
    def test_services_symlink_nginx_if_it_doesnt_exists(
        self, os, print_function
    ):
        os.path.isfile.return_value = False
        with self.assertRaises(ValueError) as er:
            fabfile.services_symlink_nginx(self.prod_env)

        print_function.assert_called_once_with(
            "Symlinking nginx"
        )

        self.assertEqual(
            str(er.exception),
            "we expect an nginx conf to exist at \
/usr/local/ohc/elcid-some_branch/etc/nginx.conf"
        )

        os.path.isfile.assert_called_once_with(
            "/usr/local/ohc/elcid-some_branch/etc/nginx.conf"
        )

    @mock.patch('fabfile.local')
    @mock.patch('fabfile.os')
    def test_services_symlink_nginx_if_exists(
        self, os, local, print_function
    ):
        os.path.isfile.return_value = True
        fabfile.services_symlink_nginx(self.prod_env)

        os.path.isfile.assert_called_once_with(
            "/usr/local/ohc/elcid-some_branch/etc/nginx.conf"
        )
        first_call = local.call_args_list[0][0][0]
        self.assertEqual(
            first_call,
            "sudo rm /etc/nginx/sites-enabled/elcid"
        )

        second_call = local.call_args_list[1][0][0]
        self.assertEqual(
            second_call,
            "sudo ln -s /usr/local/ohc/elcid-some_branch/etc/nginx.conf \
/etc/nginx/sites-enabled/elcid"
        )

    @mock.patch('fabfile.os')
    def test_services_symlink_upstart_if_it_doesnt_exists(
        self, os, print_function
    ):
        os.path.isfile.return_value = False
        with self.assertRaises(ValueError) as er:
            fabfile.services_symlink_upstart(self.prod_env)

        print_function.assert_called_once_with("Symlinking upstart")
        self.assertEqual(
            str(er.exception),
            "we expect an upstart conf to exist \
/usr/local/ohc/elcid-some_branch/etc/upstart.conf"
        )

        os.path.isfile.assert_called_once_with(
            "/usr/local/ohc/elcid-some_branch/etc/upstart.conf"
        )

    @mock.patch('fabfile.local')
    @mock.patch('fabfile.os')
    def test_services_symlink_upstart_if_exists(
        self, os, local, print_function
    ):
        os.path.isfile.return_value = True
        fabfile.services_symlink_upstart(self.prod_env)

        os.path.isfile.assert_called_once_with(
            "/usr/local/ohc/elcid-some_branch/etc/upstart.conf"
        )
        first_call = local.call_args_list[0][0][0]
        self.assertEqual(
            first_call,
            "sudo rm -f /etc/init/elcid.conf"
        )

        second = local.call_args_list[1][0][0]
        self.assertEqual(
            second,
            "sudo ln -s /usr/local/ohc/elcid-some_branch/etc/upstart.conf \
/etc/init/elcid.conf"
        )

    @mock.patch('fabfile.local')
    def test_sevices_create_local_settings(
        self, local, print_function
    ):
        some_dir = tempfile.mkdtemp()
        project_dir = "{}/elcid".format(some_dir)
        os.mkdir(project_dir)
        with mock.patch(
            "fabfile.Env.project_directory", new_callable=mock.PropertyMock
        ) as prop:
            prop.return_value = some_dir
            private_settings = dict(
                additional_settings={"Some": "'settings'"}
            )
            fabfile.services_create_local_settings(
                self.prod_env, private_settings
            )

        local_settings_file = "{}/local_settings.py".format(project_dir)
        with open(local_settings_file) as l:
            output_file = l.read()

        self.assertIn("Some = 'settings'", output_file)
        self.assertIn("'NAME': 'elcid_some_branch'", output_file)

        local.assert_called_once_with(
            "rm -f {}".format(local_settings_file)
        )

    @mock.patch('fabfile.local')
    def test_services_create_gunicorn_conf(
        self, local, print_function
    ):
        some_dir = tempfile.mkdtemp()
        project_dir = "{}/etc".format(some_dir)
        os.mkdir(project_dir)
        with mock.patch(
            "fabfile.Env.project_directory", new_callable=mock.PropertyMock
        ) as prop:
            prop.return_value = some_dir
            fabfile.services_create_gunicorn_conf(
                self.prod_env
            )
        print_function.assert_called_once_with('Creating gunicorn conf')
        gunicorn_conf_file = "{}/gunicorn.conf".format(project_dir)
        with open(gunicorn_conf_file) as l:
            output_file = l.read()

        # make sure we're executing gunicorn with our project directory
        self.assertIn("elcid-some_branch/bin/gunicorn", output_file)
        local.assert_called_once_with(
            "rm -f {}".format(gunicorn_conf_file)
        )

    @mock.patch('fabfile.local')
    def test_services_create_celery_conf(
        self, local, print_function
    ):
        some_dir = tempfile.mkdtemp()
        project_dir = "{}/etc".format(some_dir)
        os.mkdir(project_dir)
        with mock.patch(
            "fabfile.Env.project_directory", new_callable=mock.PropertyMock
        ) as prop:
            prop.return_value = some_dir
            fabfile.services_create_celery_conf(
                self.prod_env
            )
        print_function.assert_called_once_with('Creating celery conf')
        celery_conf_file = "{}/celery.conf".format(project_dir)
        with open(celery_conf_file) as l:
            output_file = l.read()

        # make sure we're executing celery with our project directory
        self.assertIn(
            "elcid-some_branch/bin/python manage.py celery worker", output_file
        )
        local.assert_called_once_with(
            "rm -f {}".format(celery_conf_file)
        )

    @mock.patch('fabfile.local')
    def test_services_create_upstart_conf(self, local, print_function):
        some_dir = tempfile.mkdtemp()
        project_dir = "{}/etc".format(some_dir)
        os.mkdir(project_dir)
        with mock.patch(
            "fabfile.Env.project_directory", new_callable=mock.PropertyMock
        ) as prop:
            prop.return_value = some_dir
            fabfile.services_create_upstart_conf(
                self.prod_env
            )

        upstart_conf_file = "{}/upstart.conf".format(project_dir)
        with open(upstart_conf_file) as l:
            output_file = l.read()
        print_function.assert_called_once_with('Creating upstart conf')
        # make sure we're executing gunicorn with our project directory
        self.assertIn("elcid-some_branch/bin/activate;", output_file)
        local.assert_called_once_with(
            "rm -f {}".format(upstart_conf_file)
        )


@mock.patch('fabfile.print', create=True)
@mock.patch('fabfile.local')
class RestartTestCase(FabfileTestCase):
    def test_restart_supervisord(
        self, local, print_function
    ):
        fabfile.restart_supervisord(self.prod_env)
        print_function.assert_called_once_with("Restarting supervisord")
        first_call = local.call_args_list[0][0][0]
        self.assertEqual(
            first_call, 'pkill super; pkill gunic; pkill celery'
        )
        second_call = local.call_args_list[1][0][0]
        expected_second_call = "/home/ohc/.virtualenvs/elcid-some_branch/bin\
/supervisord -c /usr/local/ohc/elcid-some_branch/etc/production.conf"
        self.assertEqual(second_call, expected_second_call)

    @mock.patch('fabfile.time')
    def test_restart_supervisord_with_one_failure(
        self, time, local, print_function
    ):
        local.side_effect = [
            None, ValueError("failed"), None
        ]
        fabfile.restart_supervisord(self.prod_env)
        print_function.assert_called_once_with("Restarting supervisord")
        first_call = local.call_args_list[0][0][0]
        self.assertEqual(
            first_call, 'pkill super; pkill gunic; pkill celery'
        )
        second_call = local.call_args_list[1][0][0]
        expected_second_call = "/home/ohc/.virtualenvs/elcid-some_branch/bin\
/supervisord -c /usr/local/ohc/elcid-some_branch/etc/production.conf"
        self.assertEqual(second_call, expected_second_call)
        time.sleep.assert_called_once_with(10)
        third_call = local.call_args_list[2][0][0]
        expected_third_call = "/home/ohc/.virtualenvs/elcid-some_branch/bin\
/supervisord -c /usr/local/ohc/elcid-some_branch/etc/production.conf"
        self.assertEqual(third_call, expected_third_call)

    def test_restart_nginx(self, local, print_function):
        fabfile.restart_nginx()
        print_function.assert_called_once_with('Restarting nginx')
        local.assert_called_once_with("sudo service nginx restart")


@mock.patch("fabfile.print", create=True)
@mock.patch("fabfile.get_private_settings")
@mock.patch("fabfile.run_management_command")
@mock.patch("fabfile.put")
@mock.patch("fabfile.env")
@mock.patch("fabfile.os")
@mock.patch("fabfile.datetime")
@mock.patch("fabfile.local")
class CopyBackupTestCase(FabfileTestCase):
    def test_backup_and_copy(
        self,
        local,
        dt,
        os,
        env,
        put,
        run_management_command,
        get_private_settings,
        print_function
    ):
        get_private_settings.return_value(dict(
            host_string="121.1.1.1",
            remote_passwordpassword="some_password"
        ))
        dt.datetime.now.return_value = datetime.datetime(
            2017, 9, 7
        )
        os.path.isfile.return_value = True
        fabfile.backup_and_copy(self.prod_env.branch)
        lp = "/usr/local/ohc/var/back.07.09.2017.00.00.elcid_some_branch.sql.tar.gz"
        rp = "/usr/local/ohc/var/live/back.07.09.2017.00.00.elcid_some_branch.sql.tar.gz"
        put.assert_called_once_with(
            local_path=lp,
            remote_path=rp
        )

    def test_backup_and_copy_no_backup(
        self,
        local,
        dt,
        os,
        env,
        put,
        run_management_command,
        get_private_settings,
        print_function
    ):
        get_private_settings.return_value(dict(
            host_string="121.1.1.1",
            password="some_password"
        ))
        os.path.isfile.return_value = False

        with mock.patch(
            "fabfile.Env.backup_name", new_callable=mock.PropertyMock
        ) as prop:
            prop.return_value = "some_backup"
            with self.assertRaises(ValueError) as ve:
                fabfile.backup_and_copy(self.prod_env.branch)

                self.assertRaises(
                    str(ve.exception), "unable to find backup some_backup"
                )


@mock.patch("fabfile.json")
@mock.patch("fabfile.os")
class GetPrivateSettingsTestCase(OpalTestCase):
    def test_unable_to_find_file(self, os, json):
        os.path.isfile.return_value = False

        with self.assertRaises(ValueError) as e:
            fabfile.get_private_settings()

        self.assertEqual(
            str(e.exception),
            "unable to find additional settings at \
/usr/local/ohc/private_settings.json"
        )

    def test_db_password_not_present(self, os, json):
        m = mock.mock_open()
        fab_open = "fabfile.open"
        json.load.return_value = {}
        with mock.patch(fab_open, m, create=True):
            with self.assertRaises(ValueError) as e:
                fabfile.get_private_settings()

        self.assertEqual(
            str(e.exception),
            "we require 'db_password' in your private settings"
        )

    def test_additional_settings_present(self, os, json):
        m = mock.mock_open()
        fab_open = "fabfile.open"
        json.load.return_value = dict(
            db_password="something"
        )
        with mock.patch(fab_open, m, create=True):
            with self.assertRaises(ValueError) as e:
                fabfile.get_private_settings()

        self.assertEqual(
            str(e.exception),
            "we require 'additional_settings dict (even if its empty)' in \
your private settings"
        )

    def test_host_string(self, os, json):
        m = mock.mock_open()
        fab_open = "fabfile.open"
        json.load.return_value = dict(
            db_password="something",
            additional_settings={},
            remote_password=None
        )
        with mock.patch(fab_open, m, create=True):
            with self.assertRaises(ValueError) as e:
                fabfile.get_private_settings()

        self.assertEqual(
            str(e.exception),
            "we expect host string to be set, this should be 127.0.0.1 on test, or \
the address you want to sync to on prod in your private settings"
        )

    def test_remote_password(self, os, json):
        m = mock.mock_open()
        fab_open = "fabfile.open"
        json.load.return_value = dict(
            db_password="something",
            additional_settings={},
            host_string="some_str"
        )
        with mock.patch(fab_open, m, create=True):
            with self.assertRaises(ValueError) as e:
                fabfile.get_private_settings()

        self.assertEqual(
            str(e.exception),
            "we require 'remote_password' in your private settings"
        )

    def test_get_private_settings(self, os, json):
        m = mock.mock_open()
        fab_open = "fabfile.open"
        expected = dict(
            db_password="something",
            additional_settings={},
            host_string="some_str",
            remote_password=None
        )
        json.load.return_value = expected
        with mock.patch(fab_open, m, create=True):
            result = fabfile.get_private_settings()

        self.assertEqual(result, expected)


class DeployTestCase(FabfileTestCase):
    @mock.patch("fabfile.Env")
    @mock.patch("fabfile.get_private_settings")
    @mock.patch("fabfile.pip_create_virtual_env")
    @mock.patch("fabfile.pip_set_project_directory")
    @mock.patch("fabfile.pip_install_requirements")
    @mock.patch("fabfile.postgres_create_database")
    @mock.patch("fabfile.postgres_load_database")
    @mock.patch("fabfile.services_symlink_nginx")
    @mock.patch("fabfile.services_symlink_upstart")
    @mock.patch("fabfile.services_create_local_settings")
    @mock.patch("fabfile.services_create_upstart_conf")
    @mock.patch("fabfile.services_create_celery_conf")
    @mock.patch("fabfile.services_create_gunicorn_conf")
    @mock.patch("fabfile.run_management_command")
    @mock.patch("fabfile.restart_supervisord")
    @mock.patch("fabfile.restart_nginx")
    def test_deploy_no_backup(
        self,
        restart_nginx,
        restart_supervisord,
        run_management_command,
        services_create_gunicorn_conf,
        services_create_celery_conf,
        services_create_upstart_conf,
        services_create_local_settings,
        services_symlink_upstart,
        services_symlink_nginx,
        postgres_load_database,
        postgres_create_database,
        pip_install_requirements,
        pip_set_project_directory,
        pip_create_virtual_env,
        get_private_settings,
        env_constructor
    ):
        pv = dict(
            host_string="0.0.0.0"
        )
        get_private_settings.return_value = pv
        env_constructor.return_value = self.prod_env
        fabfile._deploy("some_branch")
        env_constructor.assert_called_once_with(
            "some_branch", remove_existing=False
        )
        self.assertTrue(get_private_settings.called)
        get_private_settings.assert_called_once_with()
        self.assertEqual(
            fabfile.env.host_string,
            "0.0.0.0"
        )
        pip_create_virtual_env.assert_called_once_with(self.prod_env)
        pip_set_project_directory.assert_called_once_with(self.prod_env)
        pip_install_requirements.assert_called_once_with(self.prod_env)
        postgres_create_database.assert_called_once_with(self.prod_env)
        self.assertFalse(postgres_load_database.called)
        services_symlink_nginx.assert_called_once_with(self.prod_env)
        services_symlink_upstart.assert_called_once_with(self.prod_env)
        services_create_local_settings.assert_called_once_with(self.prod_env, pv)
        services_create_celery_conf.assert_called_once_with(self.prod_env)
        services_create_gunicorn_conf.assert_called_once_with(self.prod_env)
        services_create_upstart_conf.assert_called_once_with(self.prod_env)
        self.assertEqual(
            run_management_command.call_count, 3
        )
        first_call = run_management_command.call_args_list[0][0]
        self.assertEqual(
            first_call[0], "collectstatic --noinput"
        )

        self.assertEqual(
            first_call[1], self.prod_env
        )

        second_call = run_management_command.call_args_list[1][0]
        self.assertEqual(
            second_call[0], "migrate"
        )

        self.assertEqual(
            second_call[1], self.prod_env
        )

        third_call = run_management_command.call_args_list[2][0]
        self.assertEqual(
            third_call[0], "load_lookup_lists"
        )

        self.assertEqual(
            third_call[1], self.prod_env
        )
        restart_supervisord.assert_called_once_with(self.prod_env)
        restart_nginx.assert_called_once_with()

    @mock.patch("fabfile.os")
    @mock.patch("fabfile.Env")
    @mock.patch("fabfile.get_private_settings")
    @mock.patch("fabfile.pip_create_virtual_env")
    @mock.patch("fabfile.pip_set_project_directory")
    @mock.patch("fabfile.pip_install_requirements")
    @mock.patch("fabfile.postgres_create_database")
    @mock.patch("fabfile.postgres_load_database")
    @mock.patch("fabfile.services_symlink_nginx")
    @mock.patch("fabfile.services_symlink_upstart")
    @mock.patch("fabfile.services_create_local_settings")
    @mock.patch("fabfile.services_create_celery_conf")
    @mock.patch("fabfile.services_create_upstart_conf")
    @mock.patch("fabfile.services_create_gunicorn_conf")
    @mock.patch("fabfile.run_management_command")
    @mock.patch("fabfile.restart_supervisord")
    @mock.patch("fabfile.restart_nginx")
    def test_deploy_backup(
        self,
        restart_nginx,
        restart_supervisord,
        run_management_command,
        services_create_gunicorn_conf,
        services_create_upstart_conf,
        services_create_celery_conf,
        services_create_local_settings,
        services_symlink_upstart,
        services_symlink_nginx,
        postgres_load_database,
        postgres_create_database,
        pip_install_requirements,
        pip_set_project_directory,
        pip_create_virtual_env,
        get_private_settings,
        env_constructor,
        os
    ):
        pv = dict(
            host_string="0.0.0.0"
        )
        get_private_settings.return_value = pv
        env_constructor.return_value = self.prod_env
        os.path.isfile.return_value = True
        fabfile._deploy("some_branch", "some_backup")

        os.path.isfile.assert_called_once_with("some_backup")
        env_constructor.assert_called_once_with(
            "some_branch", remove_existing=False
        )
        self.assertTrue(get_private_settings.called)
        get_private_settings.assert_called_once_with()
        self.assertEqual(
            fabfile.env.host_string,
            "0.0.0.0"
        )
        pip_create_virtual_env.assert_called_once_with(self.prod_env)
        pip_set_project_directory.assert_called_once_with(self.prod_env)
        pip_install_requirements.assert_called_once_with(self.prod_env)

        postgres_create_database.assert_called_once_with(self.prod_env)
        postgres_load_database.assert_called_once_with(
            "some_backup", self.prod_env
        )
        services_symlink_nginx.assert_called_once_with(self.prod_env)
        services_symlink_upstart.assert_called_once_with(self.prod_env)
        services_create_local_settings.assert_called_once_with(self.prod_env, pv)
        services_create_celery_conf(self.prod_env)
        services_create_gunicorn_conf.assert_called_once_with(self.prod_env)
        services_create_upstart_conf.assert_called_once_with(self.prod_env)
        self.assertEqual(
            run_management_command.call_count, 3
        )
        first_call = run_management_command.call_args_list[0][0]
        self.assertEqual(
            first_call[0], "collectstatic --noinput"
        )

        self.assertEqual(
            first_call[1], self.prod_env
        )

        second_call = run_management_command.call_args_list[1][0]
        self.assertEqual(
            second_call[0], "migrate"
        )

        self.assertEqual(
            second_call[1], self.prod_env
        )

        third_call = run_management_command.call_args_list[2][0]
        self.assertEqual(
            third_call[0], "load_lookup_lists"
        )

        self.assertEqual(
            third_call[1], self.prod_env
        )

        restart_supervisord.assert_called_once_with(self.prod_env)
        restart_nginx.assert_called_once_with()

    @mock.patch("fabfile.os")
    @mock.patch("fabfile.Env")
    @mock.patch("fabfile.get_private_settings")
    @mock.patch("fabfile.pip_create_virtual_env")
    @mock.patch("fabfile.pip_set_project_directory")
    @mock.patch("fabfile.pip_install_requirements")
    @mock.patch("fabfile.postgres_create_database")
    @mock.patch("fabfile.postgres_load_database")
    @mock.patch("fabfile.services_symlink_nginx")
    @mock.patch("fabfile.services_symlink_upstart")
    @mock.patch("fabfile.services_create_local_settings")
    @mock.patch("fabfile.services_create_gunicorn_conf")
    @mock.patch("fabfile.run_management_command")
    @mock.patch("fabfile.restart_supervisord")
    @mock.patch("fabfile.restart_nginx")
    def test_deploy_backup_raises(
        self,
        restart_nginx,
        restart_supervisord,
        run_management_command,
        services_create_gunicorn_conf,
        services_create_local_settings,
        services_symlink_upstart,
        services_symlink_nginx,
        postgres_load_database,
        postgres_create_database,
        pip_install_requirements,
        pip_set_project_directory,
        pip_create_virtual_env,
        get_private_settings,
        env_constructor,
        os
    ):
        # mock everything because if this fails, we don't want it to
        # accidentally run roughshod on our env
        os.path.isfile.return_value = False
        with self.assertRaises(ValueError) as er:
            fabfile._deploy("some_branch", "some_nonexistent_backup")

        self.assertEqual(
            str(er.exception),
            "unable to find backup some_nonexistent_backup"
        )


class DeployTestTestCase(FabfileTestCase):
    @mock.patch("fabfile.infer_current_branch")
    @mock.patch("fabfile.Env")
    @mock.patch("fabfile._deploy")
    @mock.patch("fabfile.run_management_command")
    @mock.patch("fabfile.print", create=True)
    def test_deploy_test(
        self,
        print_function,
        run_management_command,
        deploy,
        env_constructor,
        infer_current_branch
    ):
        infer_current_branch.return_value = "new_branch"
        env_constructor.return_value = self.prod_env
        run_management_command.return_value = "some status"
        fabfile.deploy_test("some_backup")
        deploy.assert_called_once_with(
            "new_branch", "some_backup", remove_existing=True
        )
        env_constructor.assert_called_once_with("new_branch")

        self.assertEqual(
            print_function.call_count, 4
        )
        first_call = print_function.call_args_list[0][0][0]
        self.assertEqual(
            first_call, "=" * 20
        )

        second_call = print_function.call_args_list[1][0][0]
        self.assertEqual(
            second_call, "new environment was"
        )

        third_call = print_function.call_args_list[2][0][0]
        self.assertEqual(
            third_call, "some status"
        )

        fourth_call = print_function.call_args_list[3][0][0]
        self.assertEqual(
            fourth_call, "=" * 20
        )


@mock.patch("fabfile.get_private_settings")
class ValidatePrivateSettingsTestCase(FabfileTestCase):
    def test_error_on_no_host(self, get_private_settings):
        get_private_settings.return_value = dict(password="something")
        with self.assertRaises(ValueError) as er:
            fabfile.validate_private_settings()

        self.assertEqual(
            str(er.exception),
            'we need a host string inorder to scp data to a backup server'
        )

    def test_error_on_no_password(self, get_private_settings):
        get_private_settings.return_value = dict(host_string="something")
        with self.assertRaises(ValueError) as er:
            fabfile.validate_private_settings()

        self.assertEqual(
            str(er.exception),
            'we need the password of the backup server inorder to scp data \
to a backup server'
        )

    def test_no_error_when_valid(self, get_private_settings):
        get_private_settings.return_value = dict(
            host_string="something",
            password="password"
        )


@mock.patch('fabfile.print', create=True)
class DiffStatusTestCase(FabfileTestCase):
    def get_status(self, **kwargs):
        return dict(
            all_time=dict(
                demographics=1
            ),
            last_week=dict(
                demographics=1
            )
        )

    def test_same(self, print_function):
        fabfile.diff_status(
            json.dumps(self.get_status()),
            json.dumps(self.get_status())
        )
        self.assertEqual(print_function.call_count, 4)
        all_calls = print_function.call_args_list
        self.assertEqual(
            all_calls[0][0][0],
            'looking at all_time'
        )

        self.assertEqual(
            all_calls[1][0][0],
            'no difference'
        )

        self.assertEqual(
            all_calls[2][0][0],
            'looking at last_week'
        )

        self.assertEqual(
            all_calls[3][0][0],
            'no difference'
        )

    def test_new_status_new_subrecord(self, print_function):
        new_status = self.get_status()
        new_status["all_time"]["diagnoses"] = 2
        fabfile.diff_status(
            json.dumps(self.get_status()),
            json.dumps(new_status)
        )
        self.assertEqual(print_function.call_count, 4)
        all_calls = print_function.call_args_list
        self.assertEqual(
            all_calls[0][0][0],
            'looking at all_time'
        )

        self.assertEqual(
            all_calls[1][0][0],
            'missing diagnoses from old'
        )

        self.assertEqual(
            all_calls[2][0][0],
            'looking at last_week'
        )

        self.assertEqual(
            all_calls[3][0][0],
            'no difference'
        )

    def test_old_status_new_subrecord(self, print_function):
        old_status = self.get_status()
        old_status["last_week"]["diagnoses"] = 2
        fabfile.diff_status(
            json.dumps(old_status),
            json.dumps(self.get_status())
        )
        self.assertEqual(print_function.call_count, 4)
        all_calls = print_function.call_args_list
        self.assertEqual(
            all_calls[0][0][0],
            'looking at all_time'
        )

        self.assertEqual(
            all_calls[1][0][0],
            'no difference'
        )

        self.assertEqual(
            all_calls[2][0][0],
            'looking at last_week'
        )

        self.assertEqual(
            all_calls[3][0][0],
            'missing diagnoses from new'
        )

    def test_different_amount(self, print_function):
        old_status = self.get_status()
        old_status["all_time"]["demographics"] = 2
        fabfile.diff_status(
            json.dumps(old_status),
            json.dumps(self.get_status())
        )
        self.assertEqual(print_function.call_count, 4)
        all_calls = print_function.call_args_list
        self.assertEqual(
            all_calls[0][0][0],
            'looking at all_time'
        )

        self.assertEqual(
            all_calls[1][0][0],
            'for demographics we used to have 2 but now have 1'
        )

        self.assertEqual(
            all_calls[2][0][0],
            'looking at last_week'
        )

        self.assertEqual(
            all_calls[3][0][0],
            'no difference'
        )


class DeployProdTestCase(FabfileTestCase):
    @mock.patch("fabfile.diff_status")
    @mock.patch("fabfile.infer_current_branch")
    @mock.patch("fabfile.datetime")
    @mock.patch("fabfile.Env")
    @mock.patch("fabfile.validate_private_settings")
    @mock.patch("fabfile.backup_and_copy")
    @mock.patch("fabfile.run_management_command")
    @mock.patch("fabfile._deploy")
    @mock.patch("fabfile.local")
    @mock.patch("fabfile.print", create=True)
    def test_deploy_prod(
        self,
        print_function,
        local,
        _deploy,
        run_management_command,
        backup_and_copy,
        validate_private_settings,
        env_constructor,
        dt,
        infer_current_branch,
        diff_status
    ):
        infer_current_branch.return_value = "new_branch"
        dt.datetime.now.return_value = datetime.datetime(
            2017, 9, 8, 10, 47
        )
        old_env = Env("old_env", remove_existing=False)
        bk = "/usr/local/ohc/var/back.08.09.2017.10.47.elcid_old_env.sql"
        backup_and_copy.return_value = bk
        new_env = Env("new_env", remove_existing=False)
        env_constructor.side_effect = [old_env, new_env]
        run_management_command.side_effect = [
            "old_status", "new_status"
        ]
        fabfile.deploy_prod("new_branch")
        validate_private_settings.assert_called_once_with()
        _deploy.assert_called_once_with(
            "new_branch", bk, remove_existing=False
        )
        backup_and_copy.called_once_with("old_env")

        self.assertEqual(
            run_management_command.call_count, 2
        )
        first_call = run_management_command.call_args_list[0][0]
        self.assertEqual(
            first_call, ("status_report", old_env,)
        )

        second_call = run_management_command.call_args_list[1][0]
        self.assertEqual(
            second_call, ("status_report", new_env,)
        )

        self.assertEqual(
            print_function.call_count, 0
        )

        diff_status.assert_called_once_with("new_status", "old_status")
        local.assert_called_once_with("rm {}".format(bk))
