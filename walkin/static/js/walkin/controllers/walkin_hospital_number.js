//
// This is our "Enter Walk-in" flow controller
//
controllers.controller(
    'WalkinHospitalNumberCtrl',
    function($scope, $modalInstance, $modal, $rootScope, $q,
             tags,
             Episode){

        $scope.model = {
            hospitalNumber : null
        }
        $scope.patient = null;

        //
        // When we've created an episode with this flow, tag it to the correct
        // teams and then kill the modal.
        //
        $scope.tag_and_close = function(episode){
            if(!episode.newItem){
                episode = new Episode(episode);
            };
            var ep = episode.makeCopy();
            ep.category_name = 'Walkin';
            ep.date_of_episode = moment();

            //
            // Pre fill some tests:
            //
            var hiv = episode.newItem('microbiology_test');

            $q.all([
                episode.save(ep),
                hiv.save({test: 'HIV Point of Care'}),
            ]).then(function(){
                episode.active = true;
                $modalInstance.close(episode);
            })

        };

        //
        // We have an initial hospital number - we can now figure out whether to
        // Add or pull over.
        //
        $scope.findByHospitalNumber = function(){
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

        //
        // Create a new patient
        //
        $scope.newPatient = function(result){
            // There is no patient with this hospital number
            // Show user the form for creating a new episode,
            // with the hospital number pre-populated
            modal = $modal.open({
                templateUrl: '/templates/modals/add_walkin_episode.html/',
                controller: 'AddEpisodeCtrl',
                size: 'lg',
                resolve: {
                    referencedata: function(Referencedata) { return Referencedata; },
                    demographics: function() {
                        return { hospital_number: $scope.model.hospitalNumber }
                    },
                    tags: function(){ return tags }
                }
            }).result.then(function(result) {
                // The user has created the episode, or cancelled
                if(result){ // We made an episode!
                    $scope.tag_and_close(result);
                }else{
                    $modalInstance.close(result);
                }
            });
        };

        //
        // Create a new episode for an existing patient
        //
        $scope.newForPatient = function(patient){
            var active_episodes = _.filter(
                _.values(patient.episodes),
                function(e){
                    return e.active;
                });
            if(active_episodes.length > 0){
                var die = false;
                _.each(active_episodes, function(e){
                    if(e.category_name == 'Inpatient'){
                        alert('Warning - Patient is a current inpatient');
                    }else if(e.category_name == 'Walkin'){
                        var episode = new Episode(e);

                        if(episode.getTags().length > 1){
                            if(episode.hasTag('walkin_doctor')){
                                alert('Patient is currently on the Walkin Doctor list');
                                die = true;
                                $scope.cancel();
                                return
                            }
                            if(episode.hasTag('walkin_triage')){
                                alert('Patient is currently on the Walkin Nurse list');
                                die = true;
                                $scope.cancel();
                                return
                            }
                            if(episode.hasTag('walkin_review')){
                                die = true;
                                if(tags.subtag == 'walkin_review'){
                                    alert('Patient is currently on the Walkin Review list');
                                    console.log('already here');
                                    $scope.cancel();
                                } else {
                                    alert('Patient is currently on the Walkin Review list. Moving them here.');
                                    var tagging = episode.tagging[0].makeCopy();
                                    tagging.walkin_review = false;
                                    tagging[tags.subtag] = true;
                                    episode.tagging[0].save(tagging).then(function(){
                                        $modalInstance.close(episode);
                                    })
                                }
                                return
                            }
                        }
                    }
                })
            }
            if(!die){
                $scope.add_for_patient(patient);
            }
        };


        //
        // Add a new episode for an existing patient. Pre-fill the relevant demographics
        //
        $scope.add_for_patient = function(patient){
            var demographics = patient.demographics[0];
            modal = $modal.open({
                templateUrl: '/templates/modals/add_walkin_episode.html/',
                controller: 'AddEpisodeCtrl',
                size: 'lg',
                resolve: {
                    referencedata: function(Referencedata) { return Referencedata; },
                    demographics: function() { return demographics; },
                    tags: function(){ return tags }
                }
            }).result.then(function(result) {
                // The user has created the episode, or cancelled
                if(result){ // We made an episode!
                    $scope.tag_and_close(result);
                }else{
                    $modalInstance.close(result);
                }
            });
        };

        // Let's have a nice way to kill the modal.
        $scope.cancel = function() {
            $modalInstance.close('cancel');
        };
    }
);
