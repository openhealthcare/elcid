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
        tags, schema, options, episode, DischargePatientService){

        $scope.tags = tags;
        $scope.episode = episode;

        var steps = [
          "diagnosis"
        ];

        $scope.steps_details = {
            discharge: {
                icon: "fa fa-street-view",
                title: "Discharge",
                subtitle: undefined
            },
            diagnosis: {
                icon: "fa fa-stethoscope",
                title: "Diagnosis",
                subtitle: undefined
            },
            antimicrobial: {
                icon: "fa fa-flask",
                title: "Antimicrobial",
                subtitle: "Please enter the <strong>drug name</strong> and the <strong>start and end dates</strong> or state that the patient was <strong>not on antimicrobials</strong>."
            },
            travel: {
                icon: "fa fa-plane",
                title: "Travel",
                subtitle: "Please enter a <strong>travel destination</strong> and <strong>dates</strong>, or state that the patient <strong>did not travel</strong>."
            },
            consultant_at_discharge: {
                icon: "fa fa-user-md",
                title: "Consultant At Discharge",
                subtitle: "Please record the <strong>consultant</strong> at discharge."
            }
        };

        var dischargePatientService = new DischargePatientService();

        var validateTravel = function(travel){
            required_all = [
                travel.destination,
                travel.dates,
            ];

            return _.every(required_all) || travel.did_not_travel;
        };

        var validateAntimicrobial = function(antimicrobial){
          required_all = [
              antimicrobial.drug,
              antimicrobial.start_date,
              antimicrobial.end_date,
          ];

          return _.every(required_all) || antimicrobial.no_antimicriobials;
        };

        $scope.currentCategory = episode.location[0].category;

        $scope.editing = dischargePatientService.getEditing(episode);

        $scope.editing.primary_diagnosis = $scope.episode.primary_diagnosis[0].makeCopy();

        window.scope = $scope;

        if($scope.is_list_view || !episode.isDischarged()){
            steps.unshift("discharge");
        }

        if($scope.episode.primary_diagnosis.length === 0){
            var primary = $scope.episode.newItem('primary_diagnosis');
            $scope.episode.primary_diagnosis[0] = primary;
        }

        if(!$scope.episode.antimicrobial.length || _.all($scope.episode.antimicrobial, function(a){
            return !validateAntimicrobial(a);
        })){
            var antimicrobial;

            if($scope.episode.antimicrobial.length){
                antimicrobial = _.last($scope.episode.antimicrobial);
            }
            else{
                antimicrobial = $scope.episode.newItem('antimicrobial');
                $scope.episode.antimicrobial[0] = antimicrobial;
            }

            $scope.editing.antimicrobial = antimicrobial.makeCopy();
            $scope.$watch("editing.antimicrobial.no_antimicriobials", function(newValue){
                _.each(["drug", "start_date", "end_date"], function(k){
                    $scope.editing.antimicrobial[k] = undefined;
                });
            });
            steps.push("antimicrobial");
        }

        if(!$scope.episode.travel.length || _.all($scope.episode.travel, function(t){
            return !validateTravel(t);
        })){
            var travel;

            if($scope.episode.travel.length){
                travel = _.last($scope.episode.travel);
            }
            else{
                travel = $scope.episode.newItem('travel');
                $scope.episode.travel[0] = travel;
            }
            $scope.$watch("editing.travel.did_not_travel", function(newValue){
                _.each(["destination", "dates"], function(k){
                    if(newValue){
                        $scope.editing.travel[k] = undefined;
                    }
                });
            });

            $scope.editing.travel = travel.makeCopy();
            steps.push("travel");
        }

        steps.push("consultant_at_discharge");
        $scope.editing.consultant_at_discharge = $scope.episode.consultant_at_discharge[0].makeCopy();

        $scope.errors = _.reduce(steps, function(mem, y){
            mem[y] = undefined;
            return mem;
        }, {});

        $scope.nextStep = function(){
            var currentIndex = _.indexOf(steps, $scope.step);

            if(currentIndex + 1 === steps.length){
                return null;
            }
            return steps[currentIndex + 1];
        };

        $scope.getCurrentForm = function(){
            return "dischargeDiagnosis";
        };

        $scope.previousStep = function(){
            var currentIndex = _.indexOf(steps, $scope.step);

            if(!currentIndex){
                return null;
            }

            return steps[currentIndex - 1];
        };

        $scope.goToPreviousStep = function(){
            $scope.step = $scope.previousStep();
        };

        // validates each step, and if we're at the last one
        // does validation and then saves
        scope.travelWarning = false;

        $scope.goToNextStep = function(form){
            var require_all, nextStep;
            if($scope.step === "diagnosis"){
                if(!form.editing_primary_diagnosis_condition.$valid){
                    form.editing_primary_diagnosis_condition.$setDirty();
                    return;
                }
            }
            if($scope.step === "travel"){
                if(!validateTravel($scope.editing.travel)){
                    $scope.$watchGroup([
                      'editing.travel.destination',
                      'editing.travel.dates',
                      'editing.travel.did_not_travel'
                    ], function(){
                        if(validateTravel($scope.editing.travel)){
                            $scope.travelWarning = false;
                        }
                    });

                    $scope.travelWarning = true;
                    return;
                }
            }
            if($scope.step === "antimicrobial"){
                if(!validateAntimicrobial($scope.editing.antimicrobial)){
                    $scope.$watchGroup([
                      'editing.antimicrobial.drug',
                      'editing.antimicrobial.start_date',
                      'editing.antimicrobial.end_date',
                      'editing.antimicrobial.no_antimicriobials'
                    ], function(){
                        if(validateAntimicrobial($scope.editing.antimicrobial)){
                            $scope.antimicrobialWarning = false;
                        }

                    });

                    $scope.antimicrobialWarning = true;
                    return;
                }
            }
            if($scope.step === "consultant_at_discharge"){
                if(!form.editing_consultant_at_discharge_consultant.$valid){
                    form.editing_consultant_at_discharge_consultant.$setDirty();
                    return;
                }
            }

            nextStep = $scope.nextStep();
            if(nextStep){
                $scope.step = nextStep;
            }
            else{
                $scope.save();
            }
        };

        if(!$scope.step){
            $scope.step = _.first(steps);
        }

        if($scope.episode.secondary_diagnosis.length === 0){
            $scope.editing.secondary_diagnosis =  [{condition: null, co_primary: false, id: 1},
                                                   {condition: null, co_primary: false, id: 2}];
        }else{
            $scope.editing.secondary_diagnosis = _.map(
                $scope.episode.secondary_diagnosis, function(sd){
                    return sd.makeCopy();
                });
        }

        $scope.confirming = false;
        $scope.is_list_view = $location.path().indexOf('/list/') === 0;
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
      	    if (name.indexOf('micro_test') !== 0) {
            		$scope[name + '_list'] = options[name];
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
            $scope.editing.secondary_diagnosis.push(d);
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

            var saves = [];
            saves.push(primary.save($scope.editing.primary_diagnosis));

            _.each(["travel", "antimicrobial", "consultant_at_discharge"], function(s){
                if(_.contains(steps, s)){
                    var to_save = episode[s][0];
                    saves.push(to_save.save($scope.editing[s]));
                }
            });

            _.each(_.filter($scope.editing.secondary_diagnosis,
                            function(sd){ return sd.condition!== null; }),
                   function(sd, index){
                       var save;
                       var secondary;

                       if(sd.consistency_token){
                           var consistency_token = sd.consistency_token;
                           secondary = _.find(
                               $scope.episode.secondary_diagnosis,
                               function(sd){
                                   return sd.consistency_token == consistency_token;
                               }
                           );
                           save = secondary.save(sd);
                       }else{
                           secondary = $scope.episode.newItem('secondary_diagnosis');
                           delete sd.id;
                           save = secondary.save(sd);
                       }
                       saves.push(save);
                   }
                  );

            dischargePatientService.discharge(episode, $scope.editing, tags).then(function(){
                $q.all(saves).then(function(){
                    if($scope.confirming){
                        growl.success('Final Diagnosis approved.');
                    }else{
                        growl.success($scope.episode.demographics[0].name + ' discharged.');
                    }
                    $scope.discharged = true;
                    $modalInstance.close('discharged');
                });
            });

        };
    });
