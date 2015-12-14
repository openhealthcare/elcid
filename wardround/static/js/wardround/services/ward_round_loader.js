angular.module('opal.wardround.services')
    .factory('wardRoundLoader', function($q, $route, $http, recordLoader, Episode) {
        return function() {
    	    var deferred = $q.defer();
          recordLoader.then(function(records){
	        $http.get('/wardround/'+$route.current.params.wardround).then(
                    function(resource) {
                        var wardround = resource.data;
                        wardround.episodes = _.map(wardround.episodes,
                                                   function(e){return new Episode(e)} );
		        deferred.resolve(wardround);
	            }, function() {
		        // handle error better
		        alert('Ward Round could not be loaded');
	            });
            });
	    return deferred.promise;
        };
    });
