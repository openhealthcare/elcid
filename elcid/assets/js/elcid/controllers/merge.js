angular.module('opal.controllers').controller('MergePatientCtrl', function(
  $scope,
  $modalInstance,
  result,
  nextStage
){
    $scope.demographics = result.demographics[0];
    $scope.merged = result.merged[0];
    $scope.nextStage = function(){
      $modalInstance.close(null)
      nextStage($scope.merged);
    };
    $scope.cancel = function() {
      $modalInstance.close(null);
    };
});
