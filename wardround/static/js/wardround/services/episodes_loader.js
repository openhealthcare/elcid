angular.module('opal.wardround.services')
    .factory('wardRoundEpisodesLoader', function($q, $route, $http){
        return function(){
            var deferred = $q.defer();
            // Load the episodes for our current ward round please
            $http.get('/wardround/'+$route.current.params.wardround+'/episodes').then(
                function(response){
                    deferred.resolve(response.data)
                },
                function() {
	            // handle error better
	            $window.alert('List schema could not be loaded');
                }
            );
            return deferred.promise;
        };
    });
