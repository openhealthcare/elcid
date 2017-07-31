angular.module('opal.services').factory('LocationWardComparator', function($routeParams){
    "use strict";

    var CATEGORIES = [
      'Inepisode', 'Review', 'Followup', 'Transferred', 'Discharged', 'Deceased'
    ];

    return [
        function(p) { return CATEGORIES.indexOf(p.location[0].category) },
        function(p) { return p.location[0].hospital },
        function(p) {
            var matches = p.location[0].ward.match(/^T(\d+)/)
            if(matches){
              var wardNumber = matches[1];
              if(matches[1].length < 2){
                return "0" + matches[1];
              }
              else{
                return matches[1];
              }
            }
            else{
              return p.location[0].ward
            }
        },
        function(p) { return parseInt(p.location[0].bed) }
    ];
});
