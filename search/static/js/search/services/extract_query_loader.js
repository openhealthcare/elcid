angular.module('opal.services').factory('extractQueryLoader', function(
  $q, $http, $window
) {
  return {
    load: function(filterId){
      var deferred = $q.defer();
      $http.get('/search/api/extract_query/' + filterId + '/').then(function(response){
        deferred.resolve(response.data);
      }, function() {
  	    // handle error better
  	    $window.alert('Extract query could not be loaded');
      });

      return deferred.promise;
    }
  };
});
