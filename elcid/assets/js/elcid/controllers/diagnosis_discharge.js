// 
// This is the controller for elCID episodes that have a
// presenting complaint/final diagnosis pair.
// 
// We do the standard discharge, then ask some more questions.
//
controllers.controller(
    'DiagnosisDischargeCtrl',
    function(
        $scope, $rootScope, $modalInstance, $modal,
        Flow,
        tags, schema, options, episode){

        $scope.editing = {
            primary_diagnosis: null
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
        
        // Let's have a nice way to kill the modal.
        $scope.cancel = function() {
	    $modalInstance.close('cancel');
        };

        $scope.save = function() {
	    $modalInstance.close('discharged');
        };
        
        initialize();
        
    });
