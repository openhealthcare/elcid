angular.module('opal.controllers').controller('HaemView', function($scope){
  "use strict";
  function getAlertInvestigations(episode){
      if(episode.microbiology_test){
        return _.filter(episode.microbiology_test, function(mt){
           return mt.alert_investigation;
        });
      }
      else{
        return [];
      }
  }

  if($scope.patient.episodes.length){
      $scope.episode.alertInvestigations = function(){
              return _.reduce($scope.patient.episodes, function(r, e){
              var alertInvestigations = getAlertInvestigations(e);
              if(alertInvestigations.length){
                  r = r.concat(alertInvestigations);
              }

              return r;
          }, []);
      };

      this.isRecentHaemInformation = function(haemInformationRow){
         var haemInformation = _.reduce($scope.patient.episodes, function(hi, e){
             var episodeHaemInfo = e.haem_information || [];
             hi = hi.concat(episodeHaemInfo);
             return hi;
         }, []);

         haemInformation = _.sortBy(haemInformation, "patient_type");

         haemInformation = _.sortBy(haemInformation, function(hi){
             var significantDate = hi.count_recovery || hi.created;
             return new Date(significantDate);
         });

         var result = {};

         _.forEach(haemInformation, function(hi){
             result[hi.patient_type] = hi.id;
         });

         return _.contains(_.values(result), haemInformationRow.id);
      };
  }
});
