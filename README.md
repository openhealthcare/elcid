eLCID
=====

eLCID is an Electronic Clinical Infection Database.

This is the implementation of the [OPAL](https://github.com/openhealthcare/opal) project in use at HTD UCLH.

[![Build
Status](https://travis-ci.org/openhealthcare/elcid.png)](https://travis-ci.org/openhealthcare/elcid)

Open source
===========
GNU Affero GPLv3

Installation
============

pip install -r requirements.txt
python manage.py syncdb --migrate
python manage.py loaddata dumps/options.json
python manage.py createinitialrevisions

(Installation - fresh machine)
------------------------------

# Expects Postgresql, openssh-server, postfix to be preinstalled
sudo apt-get install emacs curl tree nginx git virtualenvwrapper libpq-dev python-dev
. /home/ohc/.bashrc
cd /usr/local
sudo mkdir ohc
sudo chown ohc:ohc ohc/
cd ohc
mkdir -p log/supervisord
mkdir -p var/run
mkvirtualenv elcid
git clone https://github.com/openhealthcare/elcid

sudo su postgres -c "createuser ohc"
sudo su postgres -c c"reatedb elcid"
# Edit local settings to change database

sudo cp elcid/etc/upstart.conf /etc/init/elcid.conf
sudo rm /etc/nginx/sites-enabled/default
sudo ln -s $PWD/etc/nginx.conf /etc/nginx/sites-enabled/elcid
sudo /etc/init.d/nginx restart

python manage.py collectstatic

# As Above

Communications
==============
hello@openhealthcare.org.uk

http://www.openhealthcare.org.uk

https://twitter.com/ohcuk

https://groups.google.com/forum/?ohc-dev#!forum/ohc-opal

channel #ohc_dev on freenode
