#!/bin/bash
#
# ./deploy_prod.sh $branch_name $previous_branch_name [$previous_db_name]
#
fab clone_branch:$1
cd /usr/lib/ohc/elcidrfh-$1

if [ ! -z $3 ] 
then 
    fab deploy_prod:$2,$3 # $3 was given
else
    fab deploy_prod:$2 # $3 was not given
fi
