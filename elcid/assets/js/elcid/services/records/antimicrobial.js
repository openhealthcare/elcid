//
// This is our Antimicrobial model for use on the front end.
//
angular.module('opal.records')
    .factory('Antimicrobial', function($routeParams){

        return function(record){
            if(!record.id && $routeParams.slug){
              if($routeParams.slug.indexOf('walkin') === 0){
                if(!record.start_date){
                    record.start_date = moment();
                }
              }
            }
            return record;
        };

    });
