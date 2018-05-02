angular.module('opal.services')
    .factory('extractSliceSchemaLoader', function($q, $http, $window, Schema){

    return {
      load: function(){
        var deferred = $q.defer();
        $http.get('/search/api/data_dictionary/').then(function(response) {
    	    var columns = response.data;
    	    deferred.resolve(new Schema(columns));
        }, function() {
    	    // handle error better
    	    $window.alert('Data dictionary could not be loaded');
        });

        return deferred.promise;
      }
    }
});
