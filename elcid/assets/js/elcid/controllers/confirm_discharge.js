/*
* is a patient is currently on the list, give the option to discharge
*/
angular.module('opal.controllers').controller('ConfirmDischargeCtrl', function(
  $scope, $modal, $modalInstance, DischargePatientService,
  patient, episode, tags, context, nextStepController
){
    $scope.newPatient = function(result){
        // There is no patient with this hospital number
        // Show user the form for creating a new episode,
        // with the hospital number pre-populated
        modal = $modal.open({
            backdrop: 'static',
            templateUrl: '/templates/modals/add_episode.html',
            controller: nextStepController,
            size: 'lg',
            resolve: {
                referencedata: function(Referencedata) { return Referencedata; },
                demographics: function() {
                    return patient.demographics[0];
                },
                tags: function(){ return tags; }
            }
        }).result.then(function(result) {
            // The user has created the episode, or cancelled
            if(result.then){
                result.then(function(r){
                  $modalInstance.close(r);
                });
            }else{
                $modalInstance.close(result);
            }
        });
    };

   $scope.confirm = function(){
     var dischargePatientService = new DischargePatientService();
     dischargePatientService.discharge(episode, {category: "Discharged"}, tags).then(function(){
       context.removeFromList(episode);
       $scope.newPatient(patient);
     });
   };

   $scope.cancel = function(){
     $modalInstance.close();
   };
});
