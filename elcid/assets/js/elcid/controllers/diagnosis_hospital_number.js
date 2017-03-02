angular.module('opal.controllers').controller(
    'DiagnosisHospitalNumberCtrl',
    function($scope,
             $timeout,
             $modal,
             $modalInstance,
             $http,
             $q,
             Episode,
             tags,
             context,
             hospital_number
          ){

        $scope.model = {};
        if(hospital_number){
            $scope.model.hospitalNumber = hospital_number;
        }
        $scope.tags = tags;
        $scope.findByHospitalNumber = function() {
          var patientFound = function(result){
            if(result.merged && result.merged.length){
              $scope.result = result;
            }
            else{
              $scope.newForPatient(result);
            }
          };

          var patientNotFound = function(result){
            $scope.result = result;
          };

          Episode.findByHospitalNumber(
              $scope.model.hospitalNumber,
              {
                  newPatient: patientNotFound,
                  newForPatient: patientFound,
                  error: function(){
                      // This shouldn't happen, but we should probably handle it better
                      alert('ERROR: More than one patient found with hospital number');
                      $modalInstance.close(null)
                  }
              }
          );
        };

        $scope.newPatient = function(result){
            // There is no patient with this hospital number
            // Show user the form for creating a new episode,
            // with the hospital number pre-populated
            modal = $modal.open({
                backdrop: 'static',
                templateUrl: '/templates/modals/add_episode.html',
                controller: 'DiagnosisAddEpisodeCtrl',
                resolve: {
                    referencedata: function(Referencedata) { return Referencedata; },
                    demographics: function() {
                        return { hospital_number: $scope.model.hospitalNumber }
                    },
                    tags: function(){ return $scope.tags; }
                }
            }).result.then(function(result) {
                // The user has created the episode, or cancelled
                if(result.then){
                    result.then(function(r){ $modalInstance.close(r) });
                }else{
                    $modalInstance.close(result);
                }
            });
        };

        $scope.newForPatient = function(patient){
            if (patient.active_episode_id &&
                // Check to see that this episode is not "Discharged"
                patient.episodes[patient.active_episode_id].location[0].category != 'Discharged') {
                // This patient has an active episode
                $scope.newForPatientWithActiveEpisode(patient);
            } else { // This patient has no active episode
                $scope.addForPatient(patient);
            };
        };

        $scope.newForPatientWithActiveEpisode = function(patient){
            episode = new Episode(patient.episodes[patient.active_episode_id])

            if(episode.category_name !== 'Inpatient'){ // It's the wrong category - add new
                return $scope.addForPatient(patient);
            }
            var tag = $scope.tags.tag ||  $scope.tags.subtag;

            if(episode.location[0].category == 'Followup' && episode.hasTag(tag)){
              modal = $modal.open({
                  templateUrl: '/templates/modals/confirm_discharge.html',
                  controller: 'ConfirmDischargeCtrl',
                  size: 'lg',
                  resolve: {
                      patient: function() { return patient; },
                      episode: function() { return episode; },
                      tags: function(){ return $scope.tags; },
                      context: function(){ return context; },
                      nextStepController: function(){ return 'DiagnosisAddEpisodeCtrl';}
                  }
              }).result.then(
                  function(result){
                      $modalInstance.close(result);
                  },
                  function(result){
                      $modalInstance.close(result);
                });
            }
            else{
              if (episode.tagging[0][$scope.tags.tag] &&
                  ($scope.tags.subtag === "" ||
                   episode.tagging[0][$scope.tags.subtag])) {
                  // There is already an active episode for this patient
                  // with the current tag
                  $modalInstance.close(episode);
              } else {
                  // There is already an active episode for this patient but
                  // it doesn't have the current tag.
                  // Add the current Tag.
                  episode.tagging[0][$scope.tags.tag] = true;
                  if($scope.tags.subtag !== ""){
                      episode.tagging[0][$scope.tags.subtag] = true;
                  }
                  episode.tagging[0].save(episode.tagging[0].makeCopy()).then(
                      function(){
                          $modalInstance.close(episode);
                      });
              }
            }
        };

        $scope.addForPatient = function(patient){
            demographics = patient.demographics[0];

            modal = $modal.open({
                templateUrl: '/templates/modals/add_episode.html',
                controller: 'DiagnosisAddEpisodeCtrl',
                resolve: {
                    referencedata: function(Referencedata) { return Referencedata; },
                    demographics: function() { return demographics; },
                    tags: function(){ return $scope.tags; }
                }
            }).result.then(
                function(result){
                    $modalInstance.close(result);
                },
                function(result){
                    $modalInstance.close(result);
                });
        };

        $scope.cancel = function() {
            $modalInstance.close(null);
        };

    });
