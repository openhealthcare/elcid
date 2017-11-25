angular.module('opal.controllers').controller('UchFindPatientCtrl',
  function(scope, Patient, Episode, step, episode, Item, $window) {
    "use strict";

    scope.lookup_hospital_number = function() {
        Episode.findByHospitalNumber(
            scope.demographics.hospital_number,
            {
                newPatient:    scope.new_patient,
                newForPatient: scope.new_for_patient,
                error        : function(){
                    // this shouldn't happen, but we should probably handle it better
                    $window.alert('ERROR: More than one patient found with hospital number');
                }
            });
    };

    this.initialise = function(scope){
      scope.state = 'initial';
      scope.hideFooter = true;

      scope.demographics = {
        hospital_number: undefined
      };
    };

    scope.new_patient = function(result){
        scope.hideFooter = false;
        scope.state = 'editing_demographics';
    };

    scope.new_for_patient = function(rawPatient){
        var patient = new Patient(rawPatient);
        scope.demographics = patient.demographics[0];
        var openEpisodes = _.filter(_.values(patient.episodes), function(x){
          return !x.end;
        });
        var latestEpisode = _.last(_.sortBy(openEpisodes, "id"));

        if(latestEpisode){
          var editing = scope.pathway.populateEditingDict(latestEpisode);
          // angular.extend doesn't work for angular reasons
          _.each(editing, function(v, k){
            if(k.indexOf("$") !== 0){
              scope.editing[k] = v;
            }
          });
          scope.pathway.save_url = scope.pathway.save_url + "/" + patient.id + "/" + latestEpisode.id;
        }
        else{
          scope.editing.demographics = patient.demographics[0].makeCopy();
          scope.pathway.save_url = scope.pathway.save_url + "/" + patient.id;
        }
        scope.state  = 'has_demographics';
        scope.hideFooter = false;
    };

    scope.showNext = function(editing){
        return scope.state === 'has_demographics' || scope.state === 'editing_demographics';
    };

    scope.preSave = function(editing){
      if(!editing.demographics.hospital_number){
        editing.demographics.hospital_number = scope.demographics.hospital_number;
      }
    }

    this.initialise(scope);
});
