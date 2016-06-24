//
// This is our OPAT Line Assessment model for use on the front end.
//
angular.module('opal.records')
    .factory('OPATLineAssessment', function($window){

        return function(record){
            if(!record.id){
                if(!record.assessment_date){
                    record.assessment_date = moment();
                }
            }

            return record;

        }

    });
