# Developer Documentation for elCID

Welcome to elCID's dev docs. 

## Getting set up 1 - the easy way.

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

## Getting set up 2 - the hard way.

For some "reason" you don't want to just run the automated "Make me a development environment" stuff? 

Well, I'm sure you know what you're doing. 

Below are the rough steps you'd need to go from scratch to get elCID running. 

Patches always welcome, but this method is unsupported && not recommended ;) 

### (Installation - fresh machine)

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

