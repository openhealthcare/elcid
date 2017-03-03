describe('ConfirmDischargeCtrl', function(){
    "use strict";

    var $rootScope, $scope, $modal, $httpBackend, $controller;
    var modalInstance, tags, hospital_number, $q, controller;
    var DischargePatientService, context, episode, demographics;
    var patient, discharge, modalResult;

    beforeEach(module('opal.controllers'));

    beforeEach(function(){
        inject(function($injector){
            $rootScope = $injector.get('$rootScope');
            $modal = $injector.get('$modal');
            $controller = $injector.get('$controller');
        });

        $scope = $rootScope.$new();
        modalInstance = $modal.open({template: 'notatemplate'});
        modalResult = jasmine.createSpy();
        spyOn($modal, 'open').and.callFake(function(){
            return {
              result: {
                then: function(fn){
                  fn(modalResult());
                }
              }
            }
        });

        spyOn(modalInstance, 'close').and.returnValue({
          result: {
            then: modalResult
          }
        });
        context = {removeFromList: function(){}};
        DischargePatientService = jasmine.createSpy();
        discharge = jasmine.createSpy().and.returnValue({
          then: function(fn){fn();}
        })
        DischargePatientService.and.returnValue({
          discharge: discharge
        });

        demographics = [{
            hospital_number: "1",
            patient_id: "1",
            first_name: "Susan",
            surname: "Smith"
        }];

        episode = {
            id: 1,
            tagging: [{
              infectious_diseases: true,
              id_inpatients: true
            }],
            demographics: demographics,
            location: [{
                category: "Discharged"
            }],
            category_name: "Inpatient"
        };

        patient = {
            active_episode_id: "1",
            episodes: {
                1: episode
            },
            demographics: demographics
        }
        tags = {someTag: 'or other'},


        $controller('ConfirmDischargeCtrl', {
            $scope         : $scope,
            $modalInstance : modalInstance,
            hospital_number: hospital_number,
            DischargePatientService: DischargePatientService,
            context: context,
            patient: patient,
            episode: episode,
            tags: tags,
            nextStepController: "nextStep"
        });
    });

    it("should put the patient's name on scope", function(){
      expect($scope.patientName).toBe("Susan Smith");
    });

    it('should open the next modal with the controller passed in', function(){
      spyOn(context, 'removeFromList');
      spyOn($scope, 'newPatient');
      $scope.confirm();
      expect(discharge).toHaveBeenCalledWith(episode, {category: "Discharged"}, tags);
      expect(context.removeFromList).toHaveBeenCalledWith(episode.id);
      expect($scope.newPatient).toHaveBeenCalledWith(patient);
    });

    it('show open the next step with the controller passed in', function(){
      modalResult.and.returnValue('some result');
      $scope.newPatient(patient);
      expect($modal.open).toHaveBeenCalled();
      var callArgs = $modal.open.calls.argsFor(0)[0];
      expect(callArgs.controller).toEqual('nextStep');
      expect(modalInstance.close).toHaveBeenCalledWith('some result');
    });

    it('resolve a promisse if the modal returns a promise', function(){
      modalResult.and.returnValue({then: function(fn){ fn('some result') }});
      $scope.newPatient(patient);
      expect($modal.open).toHaveBeenCalled();
      var callArgs = $modal.open.calls.argsFor(0)[0];
      expect(callArgs.controller).toEqual('nextStep');
      expect(modalInstance.close).toHaveBeenCalledWith('some result');
    });

});
