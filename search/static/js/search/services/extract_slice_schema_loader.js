angular.module('opal.services')
    .factory('extractSliceSchemaLoader', function($q, $http, $window, ExtractSchema){

    return {
      load: function(){
        var deferred = $q.defer();
        $http.get('/search/api/extract_slice_schema/').then(function(response) {
    	    var columns = response.data;
    	    deferred.resolve(new ExtractSchema(columns));
        }, function() {
    	    // handle error better
    	    $window.alert('Data dictionary could not be loaded');
        });

        return deferred.promise;
      }
    }
});
