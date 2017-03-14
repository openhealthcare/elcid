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
        tags, referencedata, episode, DischargePatientService){

        $scope.tags = tags;
        $scope.episode = episode;

        $scope.steps = [
          "diagnosis"
        ];

        $scope.steps_details = {
            discharge: {
                icon: "fa fa-home",
                display_name: "Discharge",
                subtitle: undefined,
                done: false
            },
            diagnosis: {
                icon: "fa fa-stethoscope",
                display_name: "Diagnosis",
                subtitle: undefined,
                status: 'disabled',
                done: false
            },
            presenting_complaint: {
                icon: "fa fa-heartbeat",
                display_name: "Presenting Complaint",
                subtitle: "Please enter one or more symptoms",
                done: false
            },
            antimicrobial: {
                icon: "fa fa-flask",
                display_name: "Antimicrobial",
                subtitle: "Please enter the <strong>drug name</strong> and the <strong>start and end dates</strong> or state that the patient was <strong>not on antimicrobials</strong>.",
                done: false
            },
            travel: {
                icon: "fa fa-plane",
                display_name: "Travel",
                subtitle: "Please enter a <strong>travel destination</strong> and <strong>dates</strong>, or state that the patient <strong>did not travel</strong>.",
                done: false
            },
            consultant_at_discharge: {
                icon: "fa fa-user-md",
                display_name: "Consultant At Discharge",
                subtitle: "Please record the <strong>consultant</strong> at discharge.",
                done: false
            }
        };


        var dischargePatientService = new DischargePatientService();

        /*
        * a multi step model that acts a bit like a form controller for travel and
        * antimicrobial
        */
        var MultiStep = function(requiredFields, negationField, editing, episode, columnName){
            this.none = false;
            this.warning = false;

            this.remove = function(index){
              editing[columnName].splice(index, 1);
            };

            this.getRequiredFields = function(antimicrobial){
                return _.map(requiredFields, function(r){
                    return antimicrobial[r];
                });
            };

            this.newItem = function(){
                return _.reduce(this.requiredFields, function(o, f){
                    o[f] = undefined;
                    return o;
                }, {});
            };

            this.pristine = function(antimicrobial){
              return !_.some(this.getRequiredFields(antimicrobial));
            };

            this.clear = function(){
              if(this.none){
                editing[columnName] = [this.newItem()];
                editing[columnName][0][negationField] = true;
              }
              this.warning = false;
            };

            this.validate = function(antimicrobial){
              var requiredAll = this.getRequiredFields(antimicrobial);
              return _.every(requiredAll) || this.none;
            };

            // validates a whole step, e.g. all of the antimicrobial
            this.validateStep = function(){
              var toReview = $scope.editing[columnName];

              // if there's just an empty form at the end, lets ignore that
              if(toReview > 1){
                  if(this.pristine(toReview)){
                      toReview = _.first(toReview, toReview.length-1);
                  }
              }

              var invalidModels = _.filter(toReview, function(a){
                  return !this.validate(a);
              }, this);

              if(invalidModels.length){
                this.warning = true;
                return false;
              }

              return true;
            };

            this.addAnother = function(model){
                if(!this.validate(model)){
                    this.warning=true;
                }
                else{
                    if(!this.none){
                        model.submitted=true;
                        var newModel = this.newItem();
                        editing[columnName].push(newModel);
                    }
                }
            };

            this.reset = function(){
                this.warning = false;
            };

            this.save = function(){
              saves = [];

              _.each($scope.editing[columnName], function(editingItem){
                  delete editingItem.submitted;
                  delete editingItem.id;
                  if(!this.pristine(editingItem) || editingItem[negationField]){
                    episodeItem = $scope.episode.newItem(columnName);
                    saves.push(episodeItem.save(editingItem));
                  }
              }, this);

              return saves;
            };
        };

        $scope.currentCategory = episode.location[0].category;

        $scope.editing = dischargePatientService.getEditing(episode);

        if(!$scope.episode.presenting_complaint.length ||
           !$scope.episode.presenting_complaint[0].symptoms ||
           !$scope.episode.presenting_complaint[0].symptoms.length
         ){
           var presenting_complaint;

           if(!$scope.episode.presenting_complaint.length){
              presenting_complaint = $scope.episode.newItem('presenting_complaint');
           }
           else{
              presenting_complaint = $scope.episode.presenting_complaint[0];
           }

            $scope.episode.presenting_complaint = [presenting_complaint];
            $scope.editing.presenting_complaint = presenting_complaint.makeCopy();
            $scope.editing.presenting_complaint.symptoms =[];
            $scope.steps.unshift("presenting_complaint");
        }

        if(!$scope.episode.antimicrobial.length){
            $scope.antimicrobialStep = new MultiStep(
                ["drug", "start_date", "end_date"],
                "no_antimicrobials",
                $scope.editing,
                $scope.episode,
                "antimicrobial"
            );
            $scope.editing.antimicrobial = [$scope.antimicrobialStep.newItem()];
            $scope.steps.push("antimicrobial");
        }

        if(!$scope.episode.travel.length){
            $scope.travelStep = new MultiStep(
                ["dates", "destination"],
                "did_not_travel",
                $scope.editing,
                $scope.episode,
                "travel"
            );

            $scope.editing.travel = [$scope.travelStep.newItem()];

            $scope.steps.push("travel");
        }

        $scope.editing.primary_diagnosis = $scope.episode.primary_diagnosis[0].makeCopy();

        if($scope.is_list_view || !episode.isDischarged()){
            $scope.steps.push("discharge");
        }

        if($scope.episode.primary_diagnosis.length === 0){
            var primary = $scope.episode.newItem('primary_diagnosis');
            $scope.episode.primary_diagnosis[0] = primary;
        }

        if(!$scope.episode.consultant_at_discharge[0].consultant){
            $scope.editing.consultant_at_discharge = $scope.episode.consultant_at_discharge[0].makeCopy();
            $scope.steps.push("consultant_at_discharge");
        }

        $scope.errors = _.reduce($scope.steps, function(mem, y){
            mem[y] = undefined;
            return mem;
        }, {});

        $scope.processSteps = [];

        _.each($scope.steps, function(step){
            var processStep = $scope.steps_details[step];
            processStep.name = step;
            $scope.processSteps.push(processStep);
        });

        $scope.nextStep = function(){
            var currentIndex = _.indexOf($scope.steps, $scope.step);

            if(currentIndex + 1 === $scope.steps.length){
                return null;
            }
            return $scope.steps[currentIndex + 1];
        };

        $scope.previousStep = function(){
            var currentIndex = _.indexOf($scope.steps, $scope.step);

            if(!currentIndex){
                return null;
            }

            return $scope.steps[currentIndex - 1];
        };

        $scope.goToPreviousStep = function(){
            var processStep = _.find($scope.processSteps, function(processStep){
                return processStep.name === $scope.step;
            });
            processStep.done = false;
            $scope.step = $scope.previousStep();
        };

        $scope.resetFormValidation = function(someForm){
            someForm.warning = false;
        };

        $scope.resetRequired = function(someFormField){
            someFormField.$setValidity("required", true);
        };

        $scope.goToNextStep = function(form, model){
            var require_all, nextStep;
            if($scope.step === "diagnosis"){
                if(!form.primary_diagnosis_condition.$valid){
                    form.primary_diagnosis_condition.$setDirty();
                    return;
                }

            }
            if($scope.step === "travel"){
                if(!$scope.travelStep.validateStep()){
                    return;
                }
            }
            if($scope.step === "antimicrobial"){
                if(!$scope.antimicrobialStep.validateStep()){
                    return;
                }
            }
            if($scope.step === "presenting_complaint"){
                /*
                this is a work around as multiple angular ui select does not play nicely
                with ngRequired. It might be better to set each model as a different form
                */
                if(!model.presenting_complaint.symptoms.length){
                    form.presenting_complaint_symptoms.$setValidity("required", false);
                    form.presenting_complaint_symptoms.$setDirty();
                    return;
                }
            }
            if($scope.step === "consultant_at_discharge"){
                if(!form.consultant_at_discharge_consultant.$valid){
                    form.consultant_at_discharge_consultant.$setDirty();
                    return;
                }
            }

            nextStep = $scope.nextStep();
            var processStep = _.find($scope.processSteps, function(processStep){
                return processStep.name === $scope.step;
            });

            processStep.done = true;

            if(nextStep){
                $scope.step = nextStep;
            }
            else{
                $scope.save();
            }
        };

        if(!$scope.step){
            $scope.step = _.first($scope.steps);
        }

        if($scope.episode.secondary_diagnosis.length === 0){
            $scope.editing.secondary_diagnosis =  [{condition: null, co_primary: false, id: 1}];
        }else{
            $scope.editing.secondary_diagnosis = _.map(
                $scope.episode.secondary_diagnosis, function(sd){
                    var copy = sd.makeCopy();
                    copy.submitted = true;
                    return copy;
                });
        }

        $scope.confirming = false;
        $scope.validDiagnosis = false;
        $scope.is_list_view = $location.path().indexOf('/list/') === 0;
        //
        // This flag sets the visibility of the modal body
        //
        $scope.discharged = false;

        _.extend($scope, referencedata.toLookuplists());

        //
        // We should deal with the case where we're confirming discharge
        //
        if(!$scope.is_list_view){
            $scope.confirming = true;
            $scope.validDiagnosis = _.contains($scope.condition_list, $scope.episode.primary_diagnosis[0].condition);
            if(!$scope.validDiagnosis){
                $scope.oldDiagnosis = $scope.episode.primary_diagnosis[0].condition;
                $scope.editing.primary_diagnosis.condition = undefined;
            }
        }

        //
        // Add an extra Secondary diagnosis option to the list
        //
        $scope.secondaryDiagnosisWarning = false;

        $scope.addSecondary = function(){
            $scope.secondaryDiagnosisWarning = !_.every($scope.editing.secondary_diagnosis, function(x){
                return x.condition;
            });

            if(!$scope.secondaryDiagnosisWarning){
                _.each($scope.editing.secondary_diagnosis, function(e){
                    e.submitted = true;
                });

                var d = {
                    condition: null,
                    co_primary: false,
                    id: $scope.editing.secondary_diagnosis.length + 1
                };

                $scope.editing.secondary_diagnosis.push(d);
            }
        };

        $scope.removeSecondary = function($index){
            $scope.editing.secondary_diagnosis.splice(index, 1);
        }

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
            var to_save;
            var primary = episode.primary_diagnosis[0];

            if($scope.confirming){
                $scope.editing.primary_diagnosis.confirmed = true;
            }

            var saves = [];
            saves.push(primary.save($scope.editing.primary_diagnosis));

            if(_.contains($scope.steps, "consultant_at_discharge")){
                to_save = $scope.episode.consultant_at_discharge[0];
                saves.push(to_save.save($scope.editing.consultant_at_discharge));
            }

            if(_.contains($scope.steps, "presenting_complaint")){
                to_save = $scope.episode.presenting_complaint[0];
                saves.push(to_save.save($scope.editing.presenting_complaint));
            }

            if($scope.antimicrobialStep){
                saves.concat($scope.antimicrobialStep.save());
            }
            if($scope.travelStep){
                saves.concat($scope.travelStep.save());
            }

            // if they've removed an already existing diagnosis, let them delete it
            _.each($scope.episode.secondary_diagnosis, function(sd){
                if(sd.consistency_token){
                    if(!_.find($scope.editing.secondary_diagnosis)){
                        sd.destroy();
                    }
                }
            });

            // $scope.episode.presenting_complaint[0].save($scope.editing.presenting_complaint);

            _.each(_.filter($scope.editing.secondary_diagnosis,
                            function(sd){ return sd.condition!== null; }),
                   function(sd, index){
                       var save;
                       var secondary;
                       delete sd.submitted;

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
                        growl.success($scope.episode.demographics[0].first_name + ' ' + $scope.episode.demographics[0].surname + ' discharged.');
                    }
                    $scope.discharged = true;
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
            });

        };
    });
