controllers.controller(
    'TropicalLiasonEndLiason',
    function($scope,
             $modalInstance, episode,
             DischargePatientService) {

       "use strict";
        var tags = {tropical_liason: true};
        var dischargePatientService = new DischargePatientService();
        $scope.editing = dischargePatientService.getEditing(episode);

        $scope.discharge = function(){
            dischargePatientService.discharge(episode, $scope.editing, tags).then(function(){
                $modalInstance.close('discharged');
            });
        };

        $scope.cancel = function() {
      	    $modalInstance.close('cancel');
        };
    });
