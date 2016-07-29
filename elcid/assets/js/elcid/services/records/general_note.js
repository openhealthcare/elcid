//
// This is our General Note model for use on the front end.
//
angular.module('opal.records')
    .factory('GeneralNote', function(){

        return function(record){
            if(!record.id){
                if(!record.date){
                    record.date = moment()
                }
            }

            return record;

        }

    });
