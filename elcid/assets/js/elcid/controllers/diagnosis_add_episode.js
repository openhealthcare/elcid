angular.module('opal.controllers')
.controller('DiagnosisAddEpisodeCtrl', function($scope, $http, $cookieStore, $q,
  $timeout, $modal, FieldTranslater,
  $modalInstance, Episode,
  referencedata, tags, demographics) {
    var DATE_FORMAT = 'DD/MM/YYYY';

    _.extend($scope, referencedata.toLookuplists());

    // TODO - this is no longer the way location/admission date works.
    $scope.editing = {
      tagging: [{}],
      location: {
        hospital: 'UCLH'
      },
      demographics: demographics,
    };
    $scope.editing.tagging = {};

    if(tags.tag){
      $scope.editing.tagging[tags.tag] = true;
    }

    if(tags.subtag){
      $scope.editing.tagging[tags.subtag] = true;
    }

    $scope.save = function() {
      var doa;
      // TODO is this used anywhere?
      doa = $scope.editing.date_of_admission;
      if (doa) {
        if(!angular.isString(doa)){
          doa = moment(doa).format(DATE_FORMAT);
        }
      }
      var toSave = FieldTranslater.jsToPatient($scope.editing);
      toSave.date_of_admission = doa;

      // this is not good
      toSave.tagging = [toSave.tagging];

      $http.post('/api/v0.1/episode/', toSave).success(function(episode) {
        $scope.episode = new Episode(episode);
        $scope.presenting_complaint();
      });
    };

    $scope.presenting_complaint = function() {
      var deferred = $q.defer();
      $modalInstance.close(deferred.promise);

      var item = $scope.episode.newItem('presenting_complaint');
      $scope.episode.presenting_complaint[0] = item;
      modal = $modal.open({
        templateUrl: '/templates/modals/presenting_complaint.html/',
        controller: 'EditItemCtrl',
        size: 'lg',
        resolve: {
          item: function() { return item; },
          referencedata: function(Referencedata) { return Referencedata; },
          metadata: function(Metadata) { return Metadata },
          episode: function() { return $scope.episode; },
          profile: function(UserProfile) { return UserProfile }
        }
      }).result.then(
        function(){deferred.resolve($scope.episode)},
        function(){deferred.resolve($scope.episode)}
      );
    };

    $scope.cancel = function() {
      $modalInstance.close(null);
    };

  });
