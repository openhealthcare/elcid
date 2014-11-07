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

        $scope.episode = episode;
        $scope.editing = {
            primary_diagnosis  : null,
            secondary_diagnosis: [{condition: null, co_priamary: false, id: 1},
                                  {condition: null, co_priamary: false, id: 2}]

        }
        
	for (var name in options) {
	    if (name.indexOf('micro_test') != 0) {
		$scope[name + '_list'] = options[name];
	    };
	};
        
        initialize = function(){
            var classic_discharge = Flow(
                'exit', schema, options, { episode: episode }
            );
            classic_discharge.then(
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
            var d = {condition: null, co_priamary: false, id: $scope.editing.secondary_diagnosis.length + 1}
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
                    var secondaries = _.map($scope.editing.secondary_diagnosis, function(sd){
                        var secondary = $scope.episode.newItem('secondary_diagnosis');
                        delete sd.id;
                        return secondary.save(sd)
                    })
                    $q.all(secondaries).then(function(){
                        $modalInstance.close('discharged');
                    });
                });
        };
        
        initialize();
        
    });
