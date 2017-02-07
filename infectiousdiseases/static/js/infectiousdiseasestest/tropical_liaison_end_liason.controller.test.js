describe('TropicalLiaisonEndLiaison', function(){
  var $rootScope, $scope, $modalInstance, episode;
  var $controller, dischargePatientService;

  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
        $rootScope = $injector.get('$rootScope');
        $controller = $injector.get('$controller');
    });
    $scope = $rootScope.$new();
    $modalInstance = {
      close: function(){}
    };
    spyOn($modalInstance, "close");
    dischargePatientService = {
      getEditing: function(){},
      discharge: function(){}
    };
    var getDischargePatientService = function(){
      return dischargePatientService;
    };
    spyOn(dischargePatientService, "getEditing").and.returnValue({
      external_liaison_contact_details: {
        hospitalNumber: '123'
      }
    });
    spyOn(dischargePatientService, "discharge").and.returnValue({
      then: function(fn){fn();}
    });
    episode = {};
    controller = $controller('TropicalLiaisonEndLiason', {
        $scope : $scope,
        $modalInstance: $modalInstance,
        DischargePatientService: getDischargePatientService,
        episode: episode

    });
  });

  it('should set up editing', function(){
    expect($scope.editing.external_liaison_contact_details.hospitalNumber).toEqual("123");
  });

  it('should allow the user to cancel an appointment', function(){
      $scope.cancel();
      expect($modalInstance.close).toHaveBeenCalledWith("cancel");
  });

  it('should allow a user to discharge an appointment', function(){
      $scope.discharge();
      expect(dischargePatientService.discharge).toHaveBeenCalled();
  });
});
