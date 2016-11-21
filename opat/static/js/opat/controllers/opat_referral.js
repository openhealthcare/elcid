//
// This is our "Enter OPAT" flow controller
//
controllers.controller(
    'OPATReferralCtrl',
    function($scope, $modalInstance, $modal, $rootScope, $q,
             growl,
             Episode){
        $scope.model = {
            hospital_number : null
        }
        $scope.patient = null;
        $scope.message = null;

        //
        // When we've created an episode with this flow, tag it to the correct
        // teams and then kill the modal.
        //
        $scope.tag_and_close = function(episode){
            if(!episode.newItem){
                episode = new Episode(episode);
            };
            if(!episode.tagging[0].makeCopy){
                episode.tagging[0] = episode.newItem('tagging');
            }
            var ep = episode.makeCopy()
            var teams = episode.tagging[0].makeCopy();
            var location = episode.location[0].makeCopy();

            //
            // See https://github.com/openhealthcare/elcid/issues/484 -
            //
            // Becuase we have a referrals situation, we have to flush teams.
            //
            _.each(_.keys(teams), function(team){
                if(teams[team]){ teams[team] = false };
            });

            ep.category_name = 'OPAT'
            teams.opat = true;
            teams.opat_referrals = true;
            location.opat_referral = moment();

            //
            // Pre fill some tests:
            //
            var mrsa = episode.newItem('microbiology_test');
            var vte = episode.newItem('microbiology_test');

            episode.save(ep).then(function(){
                $q.all([
                    episode.tagging[0].save(teams),
                    episode.location[0].save(location),
                    mrsa.save({test: 'MRSA PCR'}),
                    vte.save({test: 'VTE Assessment'})
                ]).then(function(){
                    episode.active = true;
                    $modalInstance.close(episode);
                });
            });


        };

        //
        // We have an initial hospital number - we can now figure out whether to
        // Add or pull over.
        //
        $scope.find_by_hospital_number = function(){

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
                $scope.model.hospital_number,
                {
                    newPatient: patientNotFound,
                    newForPatient: patientFound,
                    error: function(){
			            // This shouldn't happen, but we should probably
                        // handle it better
                        msg = 'ERROR: More than one patient found with hospital number';
			            alert(msg);
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
  		templateUrl: '/opat/templates/modals/add_episode.html/',
  		controller: 'AddEpisodeCtrl',
  		resolve: {
                    referencedata: function(Referencedata) { return Referencedata; },
		    demographics: function() {
			return { hospital_number: $scope.model.hospital_number }
		    },
                    tags: function(){ return {tag: 'opat', subtag: ''} }
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
            var actually_make_new_episode = function(){
                // Offer to import the data from this episode.
				for (var eix in patient.episodes) {
					patient.episodes[eix] = new Episode(patient.episodes[eix]);
				};
				modal = $modal.open({
					templateUrl: '/templates/modals/copy_to_category.html/',
					controller: 'CopyToCategoryCtrl',
					resolve: {
              category_name: function() { return 'OPAT' },
  						patient: function() { return patient; },
					}
				}).result.then(
                    function(result) {
                        if(!_.isString(result)){
                            $scope.tag_and_close(result);
                            return
                        };
					    if (result == 'open-new') {
						    // User has chosen to open a new episode
                            $scope.add_for_patient(patient);
					    } else {
						    // User has chosen to reopen an episode, or cancelled
						    $modalInstance.close(result);
					    };
				    },
                    function(result){ $modalInstance.close(result); });
            }

            if(patient.active_episode_id && _.keys(patient.episodes).length > 0){
                opat_episodes = _.filter(patient.episodes, function(e){ return e.category_name == 'OPAT' });
                if(opat_episodes.length > 0){
                    // Tell the user that this patient is already on the opat service
                    var list_name;
                    message = "Patient is already on the OPAT ";
                    _.each(opat_episodes, function(e){
                        if(e.tagging[0].opat_referrals){
                            list_name = "Referrals list";
                        }
                        if(e.tagging[0].opat_current){
                            list_name = "Current list";
                        }
                        if(e.tagging[0].opat_followup){
                            list_name = "Follow Up list";
                        }
                    });
                    if(list_name){
                        message += list_name;
                        $scope.message = message;
                    }else{
                        $scope.add_for_patient(patient);
                    }
                }else{
                    actually_make_new_episode();
                }
            }else{
                $scope.add_for_patient(patient);
            }
        };

        //
        // Add a new episode for an existing patient. Pre-fill the relevant demographics
        //
        $scope.add_for_patient = function(patient){
            var demographics = patient.demographics[0];

	    modal = $modal.open({
		templateUrl: '/opat/templates/modals/add_episode.html/',
		controller: 'AddEpisodeCtrl',
		resolve: {
                    referencedata: function(Referencedata) { return Referencedata; },
		    demographics: function() { return demographics; },
                    tags: function(){ return {tag: 'walkin', subtag: ''}}
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
