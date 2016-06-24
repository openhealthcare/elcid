//
// This is our General Note model for use on the front end.
//
angular.module('opal.records')
    .factory('Diagnosis', function(){

        return function(record){
            if(!record.id){
                if(!record.date_of_diagnosis){
                    record.date_of_diagnosis = moment()
                }
            }

            return record;

        }

    });
