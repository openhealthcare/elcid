//
// This is our Clinical Advice model for use on the front end.
//
angular.module('opal.records')
    .factory('MicrobiologyInput', function($window){

        return function(record){
            if(!record.id){
                if(!record.initials){
                    record.initials = $window.initials;
                }
                if(!record.when){
                    record.when = moment();
                }
            }

            return record;

        }

    });
