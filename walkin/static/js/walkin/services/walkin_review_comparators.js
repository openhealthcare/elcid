angular.module('opal.services')
    .factory('WalkinReviewComparators', function(){
        //
        // These comparators are used to define a custom sort order for the
        // Walkin Review list (alphabetical)
        //
        "use strict";

        var getName = function(x){
            var surname = x.demographics[0].surname.toLowerCase()
            var first_name = x.demographics[0].first_name.toLowerCase()
            return first_name + " " + surname;
        };

        return [
            function(p){ return p.date_of_episode },
            function(p){ return getName(p) }
        ]
    })
