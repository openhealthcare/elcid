angular.module('opal.services').factory('extractQuerySchemaLoader', function(
  $q, $http, $window, ExtractSchema
){
      return {
        load: function(){
          var deferred = $q.defer();
          $http.get('/search/api/extract_query_schema/').then(function(response) {
      	    var columns = response.data;
      	    deferred.resolve(new ExtractSchema(columns));
          }, function() {
      	    // handle error better
      	    $window.alert('Extract schema could not be loaded');
          });

          return deferred.promise;
        }
      };
});
