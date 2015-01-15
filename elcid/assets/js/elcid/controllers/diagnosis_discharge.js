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
        $location,
        growl,
        Flow,
        tags, schema, options, episode){

        $scope.tags = tags;
        $scope.episode = episode;

        // 
        // This shouldn't happen as PD is a singleton, but we have old patients...
        //
        if($scope.episode.primary_diagnosis.length == 0){
            var primary = $scope.episode.newItem('primary_diagnosis');
            $scope.episode.primary_diagnosis[0] = primary;
        }
        
        $scope.editing = {
            primary_diagnosis  : $scope.episode.primary_diagnosis[0].makeCopy(),

        }
        if($scope.episode.secondary_diagnosis.length == 0){
            $scope.editing.secondary_diagnosis =  [{condition: null, co_primary: false, id: 1},
                                                   {condition: null, co_primary: false, id: 2}]
        }else{
            $scope.editing.secondary_diagnosis = _.map(
                $scope.episode.secondary_diagnosis, function(sd){
                    return sd.makeCopy();
                } )
        }
        
        $scope.confirming = false;
        $scope.is_list_view = $location.path().indexOf('/list/') == 0;
        // 
        // This flag sets the visibility of the modal body
        //
        $scope.discharged = false;
        
        // 
        // We should deal with the case where we're confirming discharge
        //
        if(!$scope.is_list_view){
            $scope.confirming = true;
        }

        // 
        // We only really need one lookuplist.
        // TODO: put these into a nicer service.
        // 
	for (var name in options) {
	    if (name.indexOf('micro_test') != 0) {
		$scope[name + '_list'] = options[name];
	    };
	};
        
        initialize = function(){
            // 
            // TODO: Get category more dynamically
            // 
            if($scope.is_list_view || !episode.isDischarged()){

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
                        if(result == 'cancel'){
                            $scope.cancel();
                        }else{
                            $scope.discharged = true;
                        }
                    },
                    function(result){ // Reject
                        $scope.cancel();
                    });
            }else{
                $scope.discharged = true;
            }
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

        // 
        // We need to save both the primary diagnosis and any secondary diagnoses.
        // The PD is simple as it's a singleton model, and we ensured it existed
        // above.
        //
        // For SDs, we need to check whether we are creating or updating, and
        // hit the appropriate .save().
        //
        // Once everything has come back from the server, growl the user and kill
        // the modal.
        // 
        $scope.save = function() {
            var primary = episode.primary_diagnosis[0];
            
            if($scope.confirming){
                $scope.editing.primary_diagnosis.confirmed = true;
            }
            
            var saves = []
            saves.push(primary.save($scope.editing.primary_diagnosis));
            _.each(_.filter($scope.editing.secondary_diagnosis,
                            function(sd){ return sd.condition!= null }),
                   function(sd, index){
                       var save

                       if(sd.consistency_token){
                           var consistency_token = sd.consistency_token;
                           var secondary = _.find(
                               $scope.episode.secondary_diagnosis,
                               function(sd){
                                   return sd.consistency_token == consistency_token;
                               }
                           );
                           save = secondary.save(sd)
                       }else{
                           var secondary = $scope.episode.newItem('secondary_diagnosis');
                           delete sd.id;
                           save = secondary.save(sd)
                       }
                       saves.push(save)
                   }
                  );
            
            $q.all(saves).then(function(){
                if($scope.confirming){
                    growl.success('Final Diagnosis approved.')
                }else{
                    growl.success($scope.episode.demographics[0].name + ' discharged.')
                }
                $modalInstance.close('discharged');
            });
        };

        $scope.invalid = function() {
            return $scope.editing.primary_diagnosis == null
        };
        
        initialize();
        
    });
