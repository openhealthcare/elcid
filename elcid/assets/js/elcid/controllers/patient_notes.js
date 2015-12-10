//
// Editing/detail page for ward round episodes
//
angular.module('opal.controllers').controller(
   'PatientDetailCtrl', function($rootScope, $scope, $cookieStore,
                                episodes, options, profile, recordLoader,
                                EpisodeDetailMixin, ngProgressLite, $q,
                                growl
                                   ){
       "use strict";

       var COOKIE_NAME = "patientNotes-inlineForm";

       $scope.episodes = _.sortBy(episodes, function(e){
           var significantDate = e.discharge_date || e.date_of_episode || e.date_of_admission;

           if(significantDate){
              significantDate = moment(significantDate).toDate();
           }
            else{
                significantDate = new Date(1900, 1, 1);
            }

           return significantDate;
       }).reverse();

       $scope.orderByDate = function(x){
          return -moment(x.when, 'DD/MM/YYYY').unix();
       };

       $scope.inlineForm = {};

       $scope.initialiseForm = function(default_arg){
           $scope.inlineForm.name = $cookieStore.get(COOKIE_NAME) || default_arg;
       };

       $scope.$watch("inlineForm.name", function(){
           if($scope.inlineForm.name){
               $cookieStore.put(COOKIE_NAME, $scope.inlineForm.name);
           }
       }, true);

       $scope.profile = profile;
       $scope.options = options;
       $scope.episode = {
           alertInvestigations: []
       };

       $scope.markAsDuplicate = function(){
           var item = $scope.episode.newItem(name, {column: $rootScope.fields.duplicate_patient});
           $scope.isDuplicate = true;
           item.save({}).then(function(){
             growl.success("Thanks, we'll take a look");
           },
           function(){
              $scope.isDuplcate = false;
           });
       };

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

       if($scope.episodes.length){
           $scope.episode = $scope.episodes[0];
           $scope.firstEpisode = $scope.episode;
           $scope.isDuplicate = $scope.episode.duplicate_patient && $scope.episode.duplicate_patient.length;

           $scope.episode.alertInvestigations = function(){
                   return _.reduce(episodes, function(r, e){
                   var alertInvestigations = getAlertInvestigations(e);
                   if(alertInvestigations.length){
                       r = r.concat(alertInvestigations);
                   }

                   return r;
               }, []);
           };

           $scope.isRecentHaemInformation = function(haemInformationRow){
              var haemInformation = _.reduce($scope.episodes, function(hi, e){
                  var episodeHaemInfo = e.haem_information || [];
                  hi = hi.concat(episodeHaemInfo)
                  return hi;
              }, []);

              haemInformation = _.sortBy(haemInformation, "patient_type");

              haemInformation = _.sortBy(haemInformation, function(hi){
                  var significantDate = hi.count_recovery || hi.created;
                  return new Date(significantDate);
              });

              result = {};

              _.forEach(haemInformation, function(hi){
                  result[hi.patient_type] = hi.id;
              });

              return _.contains(_.values(result), haemInformationRow.id);
           };

           EpisodeDetailMixin($scope);
           if($scope.episodes.length &&
               _.last($scope.episodes).microbiology_input &&
               _.last($scope.episodes).microbiology_input.length){
               $scope.lastInputId = _.last(_.last($scope.episodes).microbiology_input).id;
           }
       }

       $scope.patient = episodes[0].demographics[0];

       $scope.getEpisodeLink = function(episode){
           return "/#/episode/" + episode.id;
       };
   }
);
