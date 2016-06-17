//
// This is our OPAT Review model for use on the front end.
//
angular.module('opal.records')
    .factory('OPATReview', function($window){

        return function(record){
            if(!record.id){
                if(!record.initials){
                    record.initials = $window.initials;
                }
                if(!record.datetime){
                    record.datetime = moment();
                }
            }

            return record;

        }

    });
