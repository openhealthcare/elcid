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

      var dischargePatientService = {
        getEditing: function(){ return {some: "editing"}; },
        discharge: function(){
          return {
            then: function(fn){fn();}
          };
        }
      };
      spyOn(dischargePatientService, "getEditing").and.callThrough();

      var DischargePatientService = function(){
        return dischargePatientService;
      };

      $modalInstance = {
        close: function(){}
      };

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

      });

      it('should do close the modal with discharge', function(){

      });
    });

    describe('cancel', function(){
      it('should do close the modal with cancel', function(){

      });
    });
});
