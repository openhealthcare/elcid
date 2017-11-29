#!/bin/bash
#
# ./deploy_test.sh $branch_name $database_backup_location
#
rm -rf /usr/lib/ohc/elcidrfh-$1
fab clone_branch:$1
cd /usr/lib/ohc/elcidrfh-$1
fab deploy_test:$2
