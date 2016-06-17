//
// This is our Line model for use on the front end.
//
angular.module('opal.records')
    .factory('Line', function(){

        return function(record){
            if(!record.id){
                if(!record.insertion_date){
                    record.insertion_date = moment()
                }
            }

            return record;

        }

    });
