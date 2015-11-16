angular.module('opal.controllers').controller(
    'ClinicalAdviceForm', function($rootScope, $scope, $window, ngProgressLite){

      self.save = function(){
          ngProgressLite.set(0);
          ngProgressLite.start()
      };

});
