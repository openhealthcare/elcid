## elCID

elCID is an electronic Clinical Infection Database.

This is the implementation of the [OPAL](https://github.com/openhealthcare/opal) project in use at RFH.

It is highly customisable open source software for managing research data

[![Build
Status](https://travis-ci.org/openhealthcare/elcid-rfh.png)](https://travis-ci.org/openhealthcare/elcid-rfh)

http://elcid.openhealthcare.org.uk


##Open source

GNU Affero GPLv3

## Developing

Developer documentation is available in DEVELOPERS.md

# Deployment

deployment is done via the fab deploy command, this takes an optional key file
or defaults to using a key file called ec2.pem in the directory a level higher

the command is fab deploy or with arguments either
fab task:my.pem
fab task:key_file_name=my.pem

## Communications

hello@openhealthcare.org.uk

http://www.openhealthcare.org.uk

https://twitter.com/ohcuk

https://groups.google.com/forum/?ohc-dev#!forum/ohc-opal
