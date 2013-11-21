eLCID
=====

eLCID is an Electronic Clinical Infection Database.
Whatever. Don't ask me. I didn't name it.

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
# Some Reversion thing here?

Communications
==============
hello@openhealthcare.org.uk

http://www.openhealthcare.org.uk

https://twitter.com/ohcuk

https://groups.google.com/forum/?ohc-dev#!forum/ohc-opal

channel #ohc_dev on freenode
