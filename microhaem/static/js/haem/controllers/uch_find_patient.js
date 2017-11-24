angular.module('opal.controllers').controller('UchFindPatientCtrl',
  function(scope, Episode, step, episode, $window) {
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

    scope.new_for_patient = function(patient){
        var allTags = [];
        _.each(patient.episodes, function(episode){
          _.each(_.keys(episode.tagging[0]), function(tag){
            if(scope.metadata.tags[tag]){
              allTags.push(tag);
            }
          });
        });
        scope.allTags = _.uniq(allTags);
        scope.demographics = patient.demographics[0];
        scope.state   = 'has_demographics';
        scope.hideFooter = false;
    };
    scope.showNext = function(editing){
        return scope.state === 'has_demographics' || scope.state === 'editing_demographics';
    };

    scope.preSave = function(editing){
        // this is not great
        editing.demographics = scope.demographics;
        if(editing.demographics && editing.demographics.patient_id){
          scope.pathway.save_url = scope.pathway.save_url + "/" + editing.demographics.patient_id;
        }
    };

    this.initialise(scope);
});
