//
// This is the "Next stage" exit flow controller for OPAT patients.
//
controllers.controller(
    'WalkinDischargeCtrl',
    function(
        $scope, $modalInstance, $modal, $rootScope, $q,
        growl, Item, CopyToCategory, UserProfile, metadata, referencedata, episode, tags
    ){

        "use strict";

        $scope.episode = episode;
        $scope.meta = {
            accepted        : null,
            target_team     : null,
            results_actioned: null,
            follow_up       : null,
            management      : episode.management[0].makeCopy()
        };

        //
        // Here we conduct varous QC checks on the quality of data entered
        // Individual methods are expected to return a boolean pass/fail for
        // that check.
        //
        // qc.passes() and qc.fails() are predicate that check all the QC
        // checks at once.
        //
        $scope.qc = {
            ignore_hiv: false,
            ignore_obs: false,
            ignore_diagnosis: false,
            hiv: function(){
                if($scope.qc.ignore_hiv){ return true };
                var hivtest = _.filter(
                    $scope.episode.microbiology_test,
                    function(t){return t.name="HIV Point of Care"}
                );
                if(hivtest == []){
                    return false;
                }
                var resulted = false;
                _.each(hivtest, function(t){ if(t.result){ resulted = true }});
                return resulted;
            },
            obs: function(){
                if($scope.qc.ignore_obs){ return true };
                return $scope.episode.observation.length > 0;
            },
            passes: function(){
                return $scope.qc.hiv() && $scope.qc.obs()
            },
            fails: function(){ return !$scope.qc.passes() }
        };

        if($scope.meta.management.follow_up){ $scope.meta.follow_up = true; }

        $scope.metadata = metadata;

        _.extend($scope, referencedata.toLookuplists());

        // Make sure that the episode's tagging item is an instance not an object
        $scope.ensure_tagging = function(episode){
            if(!$scope.episode.tagging[0].makeCopy){
                $scope.episode.tagging[0] = $scope.episode.newItem('tagging',{
                    column: $rootScope.fields.tagging }
                                                                  )
            }
            return
        };

        //
        // We have entered the follow up information - save this in
        // Walk-in Management and then set the "follow up" variable.
        //
        $scope.save_follow_up = function(){
            $scope.episode.management[0].save($scope.meta.management).then(
                function(){
                    $scope.meta.follow_up = 'saved';
                }
            );
        };

        $scope.move_to_doctor = function(){
            $scope.ensure_tagging($scope.episode);
            var tagging = $scope.episode.tagging[0].makeCopy();
            tagging.walkin_triage = false;
            tagging.walkin_doctor = true;

            $scope.episode.tagging[0].save(tagging).then(function(){
                growl.success('Moved to Doctor list')
                $modalInstance.close('discharged');
            });
        };

        //
        // The doctor has finished seeing this patient - but there remain
        // some outstanding test results that they would like to review.
        //
        // * Tag the patient to the review list
        // * Set the discharge date on the Episode
        // * Close the modal and inform the user
        //
        $scope.move_to_review = function(){
            $scope.ensure_tagging($scope.episode);
            var tagging = $scope.episode.tagging[0].makeCopy();
            tagging.walkin_doctor = false;
            tagging.walkin_review = true;

            var ep = $scope.episode.makeCopy();
            ep.discharge_date = new Date();

            $scope.episode.save(ep).then(function(){
                $scope.episode.tagging[0].save(tagging).then(function(){
                    growl.success('Moved to Review list')
                    $modalInstance.close('discharged');
                });
            });
        }

        //
        // The nurse has cared for this patient and is sending them home.
        //
        // Save the nursing care metadata, the date of discharge, de-tag
        // the patient, and then open a discharge summary window for the
        // nurse to copy the episode summary.
        //
        $scope.nurse_led_care = function(){
            var nursing = $scope.episode.newItem('walkin_nurse_led_care');

            var ep = $scope.episode.makeCopy();
            ep.discharge_date = new Date();

            var to_save = [
                nursing.save({
                    reason:    $scope.meta.nurse_reason,
                    treatment: $scope.meta.treatment
                }),
            ]
            if($scope.meta.diagnosis){
                var diagnosis = $scope.episode.newItem('diagnosis');
                to_save.push(diagnosis.save({condition: $scope.meta.diagnosis}));
            }

            $scope.ensure_tagging($scope.episode);

            var tagging = $scope.episode.tagging[0].makeCopy();
            tagging.walkin_triage = false;
            tagging.walkin_doctor = false;
            tagging.walkin_review = false;

            if($scope.episode.management.length == 0 || !$scope.episode.management[0].makeCopy){
                $scope.episode.management[0] = $scope.episode.newItem('management',{
                    column: $rootScope.fields.management }
                                                                     )
            }
            var management = $scope.episode.management[0].makeCopy();
            management.results_actioned = $scope.meta.results_actioned;
            to_save.push($scope.episode.management[0].save(management));
            to_save.push($scope.episode.tagging[0].save(tagging));

            $scope.episode.save(ep).then(function(resp){
                $q.all(to_save).then(function(){
                    growl.success('Removed from Walk-in lists');
                    var modal = $modal.open({
                        templateUrl: '/dischargesummary/modals/walkinnurse/',
                        controller: 'ModalDischargeSummaryCtrl',
                        resolve: {episode: episode}
                    });
                    modal.result.then(
                      function(){
                        $modalInstance.close("discharged");
                      },
                      function(){
                        $modalInstance.close("discharged");
                      }
                  );
                });
            });
        };

        //
        // The appointment has finished with no further follow up.
        //
        // Untag this episode
        // Set the discharge date if one does not exist
        // Close the modal and inform the user
        //
        $scope.remove_from_list = function(){
            $scope.ensure_tagging($scope.episode);
            var tagging = $scope.episode.tagging[0].makeCopy();
            tagging.walkin_triage = false;
            tagging.walkin_doctor = false;
            tagging.walkin_review = false;

            var to_save = [
                $scope.episode.tagging[0].save(tagging)
            ]

            if(!episode.discharge_date){
                var ep = $scope.episode.makeCopy();
                ep.discharge_date = new Date();
                to_save.push($scope.episode.save(ep));
            }

            $q.all(to_save).then(function(){
                growl.success('Removed from Walk-in lists');
                $modalInstance.close('discharged');
            });
        }

        //
        // Copy this episode to a new inpatient episode.
        //
        // Untag this episode.
        // Tag the new episode to the selected team
        //
        $scope.admit_to_ward = function(){
            $scope.ensure_tagging($scope.episode);
            var tagging = $scope.episode.tagging[0].makeCopy();
            tagging.walkin = false;
            tagging.walkin_doctor = false;
            $scope.meta.management.follow_up = 'Admitted to ward';

            CopyToCategory($scope.episode.id, 'Inpatient').then(
                function(episode){
                    var newtagging = episode.tagging[0];
                    var newtags = {};
                    newtags[$scope.meta.target_team] = true;
                    var ep = $scope.episode.makeCopy();
                    ep.discharge_date = new Date();
                    $q.all([
                        $scope.episode.tagging[0].save(tagging),
                        $scope.episode.save(ep),
                        newtagging.save(newtags),
                        $scope.episode.management[0].save($scope.meta.management)
                    ]).then(function(){
                        var msg = 'Admitted to ' + $scope.meta.target_team + ' ward';
                        growl.success(msg);
                        $modalInstance.close('discharged');
                    })
                });
        };


        $scope._add_a_thing = function(what){
            var deferred = $q.defer();
            $scope.episode.recordEditor.newItem(what).then(
                function(r){ deferred.resolve(r) },
                function(r){ deferred.reject(r) }
            );
            $modalInstance.close(deferred.promise);
        }

        $scope.add_some_obs = function(){
            $scope._add_a_thing('observation');
        }

        $scope.add_some_diagnosis = function(){
            $scope._add_a_thing('diagnosis');
        }

        // Let's have a nice way to kill the modal.
        $scope.cancel = function() {
            $modalInstance.close('cancel');
        };
    });
