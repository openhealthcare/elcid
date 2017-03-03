describe('ElcidDischargeEpisodeCtrl', function() {
    "use strict";

    var $rootScope, $scope, $controller, controller;
    var $modalInstance, episode, tags, DischargePatientService;
    var dischargePatientService;

    beforeEach(function(){
      module('opal.controllers');
      inject(function($injector){
        $rootScope   = $injector.get('$rootScope');
        $scope = $rootScope.$new();
        $controller  = $injector.get('$controller');
      });

      dischargePatientService = {
        getEditing: function(){ return {some: "editing"}; },
        discharge: function(){
          return {
            then: function(fn){fn();}
          };
        }
      };
      spyOn(dischargePatientService, "getEditing").and.callThrough();
      spyOn(dischargePatientService, "discharge").and.callThrough();

      var DischargePatientService = function(){};
      DischargePatientService.prototype = dischargePatientService;

      $modalInstance = jasmine.createSpyObj(["close"]);

      tags = {some: "tags"};
      episode = {location: [{category: "someCategory"}]};
      controller = $controller('ElcidDischargeEpisodeCtrl', {
        $scope: $scope,
        $modalInstance: $modalInstance,
        episode: episode,
        tags: tags,
        DischargePatientService: DischargePatientService
      });
    });

    describe('initialisation', function(){
      it('it should initialise editing and the current category', function(){
        expect($scope.editing).toEqual({some: "editing"});
        expect($scope.currentCategory).toEqual("someCategory");
      });
    });

    describe('discharge', function(){
      it('should do close the modal with follow up', function(){
        $scope.editing.category = "Followup";
        $scope.discharge();
        expect(dischargePatientService.discharge).toHaveBeenCalled();
        expect($modalInstance.close).toHaveBeenCalledWith('followup');
      });

      it('should do close the modal with discharge', function(){
        $scope.editing.category = "Discharged";
        $scope.discharge();
        expect(dischargePatientService.discharge).toHaveBeenCalled();
        expect($modalInstance.close).toHaveBeenCalledWith('discharged');
      });
    });

    describe('cancel', function(){
      it('should do close the modal with cancel', function(){
        $scope.cancel();
        expect($modalInstance.close).toHaveBeenCalledWith('cancel');
      });
    });
});
