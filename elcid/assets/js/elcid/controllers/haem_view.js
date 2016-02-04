angular.module('opal.controllers').controller('HaemView', function($scope){
  "use strict";
  var vm = this;
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

  var orderByDate = function(significantDate){
     // order by -date where date could be null, so we put that at the bottom
     if(significantDate){
         return -(moment(significantDate).unix());
     }
     else{
         // this should never happen, but if it does, put it at the bottom
         return 0;
     }
  };

  vm.getClinicalAdviceDate = function(clinicalAdvice){
     return clinicalAdvice.when || clinicalAdvice.created;
  };

  vm.clinicalAdviceOrdering = function(clinicalAdvice){
     var clinicalAdviceDate = vm.getClinicalAdviceDate(clinicalAdvice);
     return orderByDate(clinicalAdviceDate);
  };

  vm.getEpisodeOrdering = function(episode){
      var significantDate = e.discharge_date || e.date_of_episode || e.date_of_admission;
      return orderByDate(significantDate)
  };

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
