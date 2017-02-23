//
// This is the eLCID custom implementation of a discharge episode controller.
// It is included from the eLCID extra aplication template as defined in
// settings.py
//
controllers.controller(
    'ElcidDischargeEpisodeCtrl',
    function($scope,
             $modalInstance, episode,
             tags, DischargePatientService) {

        var dischargePatientService = new DischargePatientService();
        $scope.editing = dischargePatientService.getEditing(episode);
        $scope.currentCategory = episode.location[0].category;

        $scope.discharge = function(){
            dischargePatientService.discharge(episode, $scope.editing, tags).then(function(){
            if($scope.editing.category === "Followup"){
              /*
              * if a patient is marked as follow up, we leave them on the list
              * view
              */
                $modalInstance.close('followup');
            }
            else{
                $modalInstance.close('discharged');
            }
          });
        };

        $scope.cancel = function() {
      	    $modalInstance.close('cancel');
        };
    });
