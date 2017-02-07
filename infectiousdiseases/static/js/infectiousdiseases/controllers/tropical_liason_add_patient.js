controllers.controller('TropicalLiasonAddPatient', function(
    $scope, $http, $modalInstance, $q, FieldTranslater, Episode
){
  "use strict";

  $scope.editing = {
    tagging: {tropical_liason: true}
  };

  $scope.save = function(){
    var newEpisode = _.pick($scope.editing, "demographics", "tagging");
    newEpisode.category_name = "Tropical Liason";
    var toSave = FieldTranslater.jsToPatient(newEpisode);

    $http.post('/api/v0.1/episode/', toSave).success(function(episode) {
      episode = new Episode(episode);
      var tropicalLiason = $scope.editing.external_liason_contact_details;
      if(_.size(tropicalLiason)){
        var liasonContactDetails = episode.external_liason_contact_details[0];
        tropicalLiason.id = liasonContactDetails.id;
        liasonContactDetails.save(tropicalLiason).then(function(){
          $modalInstance.close(episode);
        });
      }
      else{
        $modalInstance.close(episode);
      }
    });
  };

  // Let's have a nice way to kill the modal.
  $scope.cancel = function() {
      $modalInstance.close('cancel');
  };
});
