controllers.controller('TropicalLiaisonAddPatient', function(
    $scope, $http, $modalInstance, $q, FieldTranslater, Episode
){
  "use strict";

  $scope.editing = {
    tagging: {tropical_liaison: true}
  };

  $scope.save = function(){
    var newEpisode = _.pick($scope.editing, "demographics", "tagging");
    newEpisode.category_name = "Tropical Liaison";
    var toSave = FieldTranslater.jsToPatient(newEpisode);

    $http.post('/api/v0.1/episode/', toSave).success(function(episode) {
      episode = new Episode(episode);
      var tropicalLiaison = $scope.editing.external_liaison_contact_details;
      if(_.size(tropicalLiaison)){
        var liasonContactDetails = episode.external_liaison_contact_details[0];
        tropicalLiaison.id = liasonContactDetails.id;
        liasonContactDetails.save(tropicalLiaison).then(function(){
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
