describe('DiagnosisHospitalNumber', function(){
    "use strict";

    var $rootScope, $scope, $modal, $httpBackend, $controller;
    var modalInstance, tags, hospital_number, $q;

    beforeEach(module('opal.controllers'));

    beforeEach(function(){
        inject(function($injector){
            $httpBackend    = $injector.get('$httpBackend');
            $rootScope      = $injector.get('$rootScope');
            $modal          = $injector.get('$modal');
            $controller = $injector.get('$controller');
            $q           = $injector.get('$q');
        });

        $scope = $rootScope.$new();
        modalInstance = $modal.open({template: 'notatemplate'});

        $controller('DiagnosisHospitalNumberCtrl', {
            $scope         : $scope,
            $modalInstance : modalInstance,
            tags           : {"someTag": true},
            hospital_number: hospital_number,
            episode: "some episode",
            context: {ctx: 'some context'}
        });
    });

    describe('newPatient()', function() {

        it('should open the AddPatientModal and then close with cancel', function() {
            spyOn(modalInstance, 'close');
            spyOn($modal, 'open').and.callFake(function(){
                return {
                  result: {
                    then: function(fn){
                      // modal instance should only be closed when
                      // the add patient modal has been resolved
                      expect(modalInstance.close).not.toHaveBeenCalled();
                      fn('cancel');
                    }
                  }
                }
            });
            $scope.newPatient({hospital_number: '555-123'});
            expect(modalInstance.close).toHaveBeenCalledWith('cancel')
        });

        it('should pass the tags to the addpatient modal', function() {
          spyOn($modal, 'open').and.callFake(function(){
              return {
                result: {
                  then: function(fn){
                    // modal instance should only be closed when
                    // the add patient modal has been resolved
                    expect(modalInstance.close).not.toHaveBeenCalled();
                    fn('cancel');
                  }
                }
              }
          });
            spyOn(modalInstance, 'close');
            $scope.newPatient({hospital_number: '555-123'});
            var resolvers = $modal.open.calls.mostRecent().args[0].resolve
            expect(resolvers.tags()).toEqual({"someTag": true});
            expect(modalInstance.close).toHaveBeenCalled();
        });
    });

    describe('newForPatientWithActiveEpisode()', function(){
        var patientData = {
            active_episode_id: "1",
            episodes: {
                1: {
                  id: 1,
                  tagging: [{
                    infectious_diseases: true,
                    id_inpatients: true
                  }],
                  demographics: [{
                      hospital_number: "1",
                      patient_id: "1",
                  }],
                  location: [{
                      category: "Discharged"
                  }],
                  category_name: "Inpatient"
            }},
            demographics: [{
                hospital_number: "1",
                patient_id: "1",
            }]
        };

        it('if the patient is an inpatient and has no subtag, tag the episode and close', function(){
            var patient = angular.copy(patientData);
            spyOn(modalInstance, 'close');
            $scope.tags = {tag: "infectious_diseases", subtag: ""}
            $scope.newForPatientWithActiveEpisode(patient);
            expect(modalInstance.close).toHaveBeenCalled();
        });
        it('if the patient is an inpatient and has a subtag, tag the episode and close', function(){
            var patient = angular.copy(patientData);
            patient.episodes["1"].tagging[0].save = function(){
              return {
                then: function(fn){ return fn(patient); }
              };
            };
            patient.episodes["1"].tagging[0].makeCopy = function(){
                return this;
            };
            spyOn(patient.episodes["1"].tagging[0], "save").and.callThrough();
            spyOn(modalInstance, 'close');
            $scope.tags = {tag: "infectious_diseases", subtag: "id_liason"};
            $scope.newForPatientWithActiveEpisode(patient);
            expect(modalInstance.close).toHaveBeenCalled();
            expect(patient.episodes["1"].tagging[0].save).toHaveBeenCalled();
            var callArgs = patient.episodes["1"].tagging[0].save.calls.argsFor(0);
            expect(callArgs[0].id_liason).toBe(true);
        });
        it('if the patient is not an inpatient, call through', function(){
            var patient = angular.copy(patientData);
            patient.episodes["1"].category_name = "Tropical";
            spyOn($scope, "addForPatient");
            $scope.newForPatientWithActiveEpisode(patient);
            expect($scope.addForPatient).toHaveBeenCalled();
        });
        it('if the patient is marked for follow up we should call the confirm discharge modal', function(){
            var patient = angular.copy(patientData);
            patient.episodes['1'].location[0].category = "Followup";
            $scope.tags = {tag: "infectious_diseases"};
            spyOn($modal, "open").and.returnValue({result: {then: function(x, y){}}});
            $scope.newForPatientWithActiveEpisode(patient);
            expect($modal.open).toHaveBeenCalled();
            var modalArgs = $modal.open.calls.argsFor(0)[0];
            expect(modalArgs.templateUrl).toBe('/templates/modals/confirm_discharge.html');
            expect(modalArgs.controller).toBe('ConfirmDischargeCtrl');
            expect(modalArgs.resolve.context()).toEqual({ctx: 'some context'});
            expect(modalArgs.resolve.patient()).toEqual(patient);
            expect(modalArgs.resolve.episode().id).toEqual(1);
            expect(modalArgs.resolve.nextStepController()).toEqual(
              'DiagnosisAddEpisodeCtrl'
            );
            expect(modalArgs.resolve.tags()).toEqual(
              {tag: "infectious_diseases"}
            );
        });
    });

    describe('addForPatient()', function() {
      it('should call through if there is an active discharged episode.', function(){
          var deferred, callArgs;
          spyOn($scope, 'newForPatientWithActiveEpisode');

          var patientData = {
              "demographics": [
                      {
                          "consistency_token": "0beb0d46",
                          "date_of_birth": "",
                          "hospital_number": "",
                          "id": 2,
                          "name": "Mr WAT",
                          "patient_id": 2
                      }
                  ]
            };

          deferred = $q.defer();
          spyOn($modal, 'open').and.returnValue({result: deferred.promise});

          $scope.newForPatient(patientData);

          callArgs = $modal.open.calls.mostRecent().args;
          expect(callArgs.length).toBe(1);
          expect(callArgs[0].controller).toBe('DiagnosisAddEpisodeCtrl');
          var resolves = $modal.open.calls.mostRecent().args[0].resolve;
          var expected_demographics = angular.copy(patientData.demographics[0]);
          expect(resolves.demographics()).toEqual(expected_demographics);
          expect(resolves.tags()).toEqual({someTag: true});
      });

    });

});
