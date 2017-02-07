controllers.controller(
    'TropicalLiaisonEndLiason',
    function($scope,
             $modalInstance, episode,
             DischargePatientService) {

       "use strict";
        var tags = {tag: "tropical_liaison", subtag: ""};
        var dischargePatientService = new DischargePatientService();
        $scope.editing = dischargePatientService.getEditing(episode);

        $scope.discharge = function(){
            dischargePatientService.discharge(episode, $scope.editing, tags).then(function(){
                $scope.discharged = true;
                $modalInstance.close('discharged');
            });
        };

        $scope.cancel = function() {
      	    $modalInstance.close('cancel');
        };
    });
