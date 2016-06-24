//
// This is our Investigation model for use on the front end.
//
angular.module('opal.records')
    .factory('Investigation', function(){

        return function(record){
            if(!record.id){
                if(!record.date_ordered){
                    record.date_ordered = moment()
                }
            }

            return record;

        }

    });
