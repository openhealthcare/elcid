// 
// This is the controller for elCID episodes that have a
// presenting complaint/final diagnosis pair.
// 
// We do the standard discharge, then ask some more questions.
//
controllers.controller(
    'DiagnosisDischargeCtrl',
    function(
        $scope, $rootScope, $modalInstance, $modal, $q,
        Flow,
        tags, schema, options, episode){

        $scope.tags = tags;
        $scope.episode = episode;
        $scope.editing = {
            primary_diagnosis  : null,
            secondary_diagnosis: [{condition: null, co_primary: false, id: 1},
                                  {condition: null, co_primary: false, id: 2}]

        }

        // 
        // We should deal with the case where we're confirming discharge
        //
        if(episode.primary_diagnosis.length == 1){
            $scope.editing.primary_diagnosis = episode.primary_diagnosis[0].condition;
        };
        if(episode.secondary_diagnosis && episode.secondary_diagnosis.length > 0){
            $scope.editing.secondary_diagnosis = _.map(
                episode.secondary_diagnosis,
                function(d){
                    return d.makeCopy();
                }
            );
        }
        
	for (var name in options) {
	    if (name.indexOf('micro_test') != 0) {
		$scope[name + '_list'] = options[name];
	    };
	};
        
        initialize = function(){

            var classic_discharge = Flow.flow_for_verb('exit')
            var classic_result    = $modal.open({
		templateUrl: classic_discharge.template,
		controller:  classic_discharge.controller,
		resolve: {
		    episode: function() { return $scope.episode; },
                    tags   : function() { return $scope.tags; },
                    options: function() { return options; },
                    schema : function() { return schema; }
		}
	    }).result

            classic_result.then(
                function(result){ // Resolve
                    console.log('collect our extra data now !')
                    
                },
                function(result){ // Reject
                    $scope.cancel();
                });
        }


        //
        // Add an extra Secondary diagnosis option to the list
        // 
        $scope.addSecondary = function(){
            var d = {
                condition: null,
                co_primary: false,
                id: $scope.editing.secondary_diagnosis.length + 1
            };
            $scope.editing.secondary_diagnosis.push(d)
        };
        
        // Let's have a nice way to kill the modal.
        $scope.cancel = function() {
	    $modalInstance.close('cancel');
        };

        $scope.save = function() {
            var primary = episode.newItem('primary_diagnosis');
            primary.save({condition: $scope.editing.primary_diagnosis}).then(
                function(){
                    var secondaries = _.map(
                        _.filter($scope.editing.secondary_diagnosis, function(sd){ return sd.condition!= null }), 
                        function(sd){
                        var secondary = $scope.episode.newItem('secondary_diagnosis');
                        delete sd.id;
                        return secondary.save(sd)
                    })
                    $q.all(secondaries).then(function(){
                        $modalInstance.close('discharged');
                    });
                });
        };

        $scope.invalid = function() {
            return $scope.editing.primary_diagnosis == null
        };
        
        initialize();
        
    });
