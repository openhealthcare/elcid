# Developer Documentation for elCID

Welcome to elCID's dev docs. 

elCID is an implementation of the OPAL framework for Digital Clinical Services. 

The developer docs for OPAL - particularly the Your Implementation sections are your friend.

In this document we'll run through setting up a development environment, walk you through the codebase, brief you on the location of the project's governance and development toolchain.

## Getting yourself set up

If you've never worked on elCID before, this is how you get going:

### Getting set up 1 - the easy way.

elCID is fully supported by the [Open Health Care Developer Toolkit](https://github.com/openhealthcare/developer). 
Which is a fancy way to spell "Vagrant vm". 

Go over there, install that, then come back... we'll wait. 

*waits*

OK - so you installed the OHCDT ? 

Lucky for you, there is no step 2. 

Try sshing into the box and starting the dev server: 

    $ vagrant ssh
    $ workon elcid
    $ python manage.py runserver 0.0.0.0:8000

### Getting set up 2 - the hard way.

For some "reason" you don't want to just run the automated "Make me a development environment" stuff? 

Well, I'm sure you know what you're doing. 

Below are the rough steps you'd need to go from scratch to get elCID running. 

Patches always welcome, but this method is unsupported && not recommended ;) 

#### (Installation - fresh machine)

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

    pip install -r requirements.txt
    python manage.py syncdb --migrate
    python manage.py loaddata dumps/options.json
    python manage.py createinitialrevisions


## Governance

The elCID project is curated by Open Health Care and the Hospital For Tropical Diseases at University College Hospital London. There is a public record of issues on github, and strategic decisions about the direction of the project are documented there. 

## Development toolchain

The elCID project runs on Linux -> Postgres -> Python -> AngularJS -> Bootstrap. 

We use Github for source code && PR management and Waffle.io for sprint planning.

Continuous integration happens via Travis CI

Test deployments run on Heroku.

## Code Walkthrough

### .

Various documentation files (README, DEVELOPERS, CONTRIBUTING, LICENSE)

Configuration files: 

* .travis.yml -> Travis CI
* Procfile -> Heroku deployments
* requirements.txt -> Python dependencies

Scripts: 

* manage.py -> Django management tool
* Rakefile -> Dev tasks (run tests etc) 

### assets

This is a dummy directory that exists to make Heroku happy when we run collectstatic. Nothing to see here, move along.

### config

Contains configuration files for running javascript tests.

### dumps

Fixtures for things like lookup lists.

### elcid

This is the source code!

Much of this is What You Would Expect from a Django project. We'll just explain the things that are specific to OPAL/elCID here.

#### elcid/schema.py

This file contains the various schemas (sets of columns) for list views in elCID. 

#### elcid/options.py

This contains our OPAL lookuplist models.
TODO: Move these out of here or make them implementationd dependent.

#### elcid/models.py

This contains our datamodels for elCID.

These are roughly speaking, a 1-1 mapping to columns somewhere in elCID.

#### elcid/assets/js/elcid

This is where our elcid-specific controllers live.
This is basically just for discharge flow at the moment. 

### etc

Contains our production config files.

