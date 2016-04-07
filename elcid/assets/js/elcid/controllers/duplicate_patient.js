angular.module('opal.controllers').controller(
    'DuplicatePatientCtrl', function($rootScope, $scope, $window, ngProgressLite){

      self.save = function(){
          ngProgressLite.set(0);
          ngProgressLite.start()
      };

});
