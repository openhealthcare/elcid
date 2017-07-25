//
// This is the "Next stage" exit flow controller for OPAT patients.
//
controllers.controller(
    'OPATDischargeCtrl',
    function($scope, $modalInstance, $rootScope, $q,
             growl,
             Item, CopyToCategory,
             referencedata, episode, tags){

        var DATE_FORMAT = 'DD/MM/YYYY';
        var opat_rejection = $rootScope.fields['opat_rejection'];

        $scope.episode = episode;
        $scope.meta = {
            accepted: null,
            rejection: {date: moment().format(DATE_FORMAT)}
        };

        $scope.qc = {
            no_allergies: null,
            consultant: null,
            referring_team: null,
            confirmed: false,

            referral: function(){
                if($scope.episode.location[0].opat_referral_team || ($scope.qc.referring_team != null && $scope.qc.confirmed)){
                    return true
                }
                if($scope.episode.location[0].opat_referral_consultant || ($scope.qc.consultant != null && $scope.qc.confirmed)){
                    return true
                }
                return false
            },
            allergies: function(){
                if($scope.episode.allergies.length > 0){
                    return true
                }
                return $scope.qc.no_allergies != null;
            },
            fails: function(){
                return !$scope.qc.referral() || !$scope.qc.allergies()
            },
            passes: function(){
                return !$scope.qc.fails();
            }
        };

        _.extend($scope, referencedata.toLookuplists());

        // Make sure that the episode's tagging item is an instance not an object
        $scope.ensure_tagging = function(episode){
            if(!$scope.episode.tagging[0].makeCopy){
                $scope.episode.tagging[0] = $scope.episode.newItem('tagging')
            }            return
        };

        //
        // This method made more sense when we were storing metadata on a
        // singleton. now it just returns a new metadata instance.
        //
        $scope.get_meta = function(){
            return $scope.episode.newItem('opat_meta');
        }

        //
        // The patient is accepted onto the OPAT service.
        // We need to update their tagging data.
        $scope.accept = function(){
            if(!$scope.episode.tagging[0].makeCopy){
                $scope.episode.tagging[0] = $scope.episode.newItem('tagging')
            }
            var tagging = $scope.episode.tagging[0].makeCopy();
            tagging.opat_referrals = false;
            tagging.opat_current = true;
            tagging.opat = true;

            var locationdata = $scope.episode.location[0].makeCopy();
            locationdata.opat_acceptance = moment();
            if($scope.qc.consultant || $scope.qc.referring_team){
                if($scope.qc.referring_team){
                    locationdata.opat_referral_team = $scope.qc.referring_team;
                }
                if($scope.qc.consultant){
                    locationdata.opat_referral_consultant = $scope.qc.consultant;
                }
            }
            episodeChanges = $scope.episode.makeCopy();
            episodeChanges.start = locationdata.opat_acceptance;

            var saves = [
                $scope.episode.tagging[0].save(tagging),
                $scope.episode.location[0].save(locationdata),
                $scope.episode.save(episodeChanges)
            ];

            if($scope.qc.no_allergies == true){
                var allergy = $scope.episode.newItem('allergies');
                saves.push(allergy.save({drug: 'No known allergies'}));
            }

            $q.all(saves).then(function(){
                growl.success(
                    'Accepted: ' + episode.demographics[0].first_name + ' ' + episode.demographics[0].surname
                );
                $modalInstance.close('moved');
            });
        };

        $scope.click_reject = function(){
            $scope.meta.accepted = false;
            $scope.meta.review_date = moment().add(3, 'M').toDate();
            return
        }
        //
        // The patient is rejected from the OAPT service.
        // Store some extra data.
        //
        $scope.reject = function(){
            var meta = $scope.get_meta();
            var opatmetadata = meta.makeCopy();
            var rejection = $scope.episode.newItem('opat_rejection', {column: opat_rejection});
            var tagging = $scope.episode.tagging[0].makeCopy();

            $scope.ensure_tagging(episode);
            opatmetadata.review_date = $scope.meta.review_date;
            var episodeToSave = $scope.episode.makeCopy();
            episodeToSave.end = $scope.meta.rejection.date;

            tagging.opat_referrals = false;
            tagging.opat = false;

            $q.all([
                rejection.save($scope.meta.rejection),
                $scope.episode.tagging[0].save(tagging),
                meta.save(opatmetadata),
                $scope.episode.save(episodeToSave)
            ]).then(function(){
                //
                // This comment edited to add (DM): I have literally no idea what the next
                // comment means :(
                //
                // Doesn't auto update for OPAT as TAGGING is not in the default schema.
                $scope.episode.tagging[0] = tagging;
                var dateStr = $scope.meta.review_date;

                if(_.isDate(dateStr)){
                    dateStr = moment($scope.meta.review_date).format(DATE_FORMAT);
                }
                var message = 'Rejected: ' + episode.demographics[0].first_name + ' ' + episode.demographics[0].surname;
                message += '.\n Patient will come up for OPAT review after ' + dateStr;
                growl.success(message);
                $modalInstance.close('discharged');
            });

        };

        //
        // The patient is being removed from the current list because they've
        // switched to oral antibiotics
        //
        $scope.switch_to_oral = function(){
            var meta = $scope.get_meta();
            $scope.ensure_tagging($scope.episode);
            var tagging = $scope.episode.tagging[0].makeCopy();
            tagging.opat_current = false;
            tagging.opat_followup = true;

            updatedmeta = meta.makeCopy();
            updatedmeta.reason_for_stopping = $scope.meta.reason;
            updatedmeta.unplanned_stop_reason = $scope.meta.unplanned_stop;
            updatedmeta.stopping_iv_details = $scope.meta.details;
            updatedmeta.review_date       = $scope.meta.review_date;
            updatedmeta.treatment_outcome = $scope.meta.outcome;
            updatedmeta.deceased          = $scope.meta.died;
            updatedmeta.cause_of_death    = $scope.meta.cause_of_death;
            updatedmeta.death_category    = $scope.meta.death_category;
            updatedmeta.readmitted        = $scope.meta.readmitted;
            updatedmeta.treatment_outcome = $scope.meta.outcome;
            updatedmeta.notes             = $scope.meta.notes;

            var outcome = $scope.episode.newItem('opat_outcome');
            var outcomesdata = {
                patient_outcome: $scope.meta.patient_outcome,
                opat_outcome   : $scope.meta.opat_outcome,
                outcome_stage  : 'Completed Therapy',
                infective_diagnosis: $scope.meta.infective_diagnosis
            }

            // Now let's save
            $q.all([
                outcome.save(outcomesdata),
                meta.save(updatedmeta),
                $scope.episode.tagging[0].save(tagging)
            ]).then(function(){
                growl.success('Moved to Follow up: ' + episode.demographics[0].first_name + ' ' + episode.demographics[0].surname)
                $modalInstance.close('discharged');
            });
        }

        //
        // A patient has completed their OPAT therapy.
        //
        $scope.completed_therapy = function(addendum){
            var meta = $scope.get_meta();
            $scope.ensure_tagging($scope.episode);
            var tagging = $scope.episode.tagging[0].makeCopy();
            tagging.opat_current = false;
            tagging.opat_followup = false;

            updatedmeta = meta.makeCopy();

            updatedmeta.review_date       = $scope.meta.review_date;
            updatedmeta.treatment_outcome = $scope.meta.outcome;
            updatedmeta.deceased          = $scope.meta.died;
            updatedmeta.cause_of_death    = $scope.meta.cause_of_death;
            updatedmeta.death_category    = $scope.meta.death_category;
            updatedmeta.readmitted        = $scope.meta.readmitted;
            updatedmeta.treatment_outcome = $scope.meta.outcome;
            updatedmeta.notes             = $scope.meta.notes;

            ep = $scope.episode.makeCopy();
            ep.end = new Date();

            var outcome = $scope.episode.newItem('opat_outcome');
            var outcomesdata = {
                patient_outcome: $scope.meta.patient_outcome,
                opat_outcome   : $scope.meta.opat_outcome,
                outcome_stage  : 'Completed Therapy',
                infective_diagnosis: $scope.meta.infective_diagnosis
            }

            if(addendum){
                outcomesdata.outcome_stage += addendum;
            }

            // Now let's save
            $q.all([
                meta.save(updatedmeta),
                $scope.episode.tagging[0].save(tagging),
                $scope.episode.save(ep),
                outcome.save(outcomesdata)
            ]).then(function(){
                growl.success('Completed treatment: ' + episode.demographics[0].first_name + ' ' + episode.demographics[0].surname);
                $modalInstance.close('discharged');
            });
        };

        //
        // The patient is being removed from the follow up list because they're
        // going back to IV
        //
        // This means that we create a whole new OPAT episode for them !
        //
        $scope.back_to_iv = function(){
            var meta = $scope.get_meta();
            $scope.ensure_tagging($scope.episode);
            var tagging = $scope.episode.tagging[0].makeCopy();

            tagging.opat_current = false;
            tagging.opat_followup = false;
            updatedmeta = meta.makeCopy();
            updatedmeta.reason_for_stopping = $scope.meta.reason;
            updatedmeta.unplanned_stop_reason = $scope.meta.unplanned_stop;
            updatedmeta.stopping_iv_details = $scope.meta.details;

            $q.all([
                meta.save(updatedmeta),
                $scope.episode.tagging[0].save(tagging)
            ]).then(function(){
                CopyToCategory($scope.episode.id, 'OPAT').then(function(episode){
                    var newtagging = episode.tagging[0].makeCopy();
                    var locationdata = episode.location[0].makeCopy();
                    newtagging.opat = true;
                    newtagging.opat_referrals = true;
                    locationdata.opat_referral_route = 'From OPAT Follow Up';
                    locationdata.opat_referral_team = 'OPAT Team';
                    locationdata.opat_referral = new Date();
                    $q.all([
                        episode.tagging[0].save(newtagging),
                        episode.location[0].save(locationdata)
                    ]).then(function(){
                        growl.success(episode.demographics[0].first_name + ' ' + episode.demographics[0].surname + ' has been moved back to OPAT referrals');
                        $modalInstance.close('discharged');
                    })
                });
            });
        }


        // Let's have a nice way to kill the modal.
        $scope.cancel = function() {
	        $modalInstance.close('cancel');
        };
    });
