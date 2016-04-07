describe('DiagnosisHospitalNumber', function(){
    "use strict";

    var $rootScope, $scope, $modal, $httpBackend, $controller;
    var modalInstance, tags, options, hospital_number, $q;

    beforeEach(module('opal.controllers', function($provide){
        $provide.service('Options', function(){
          return {
            then: function(x){ x({}); }
          };
        });
    }));

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
            options        : options,
            tags           : {},
            hospital_number: hospital_number
        });
    });

    describe('newPatient()', function() {

        it('should open the AddPatientModal and then close with cancel', function() {
            spyOn($modal, 'open').and.callFake(function(){
                return {result: {then: function(fn){ fn('cancel') }}}
            });
            spyOn(modalInstance, 'close');
            $scope.newPatient({hospital_number: '555-123'});
            expect(modalInstance.close).toHaveBeenCalledWith('cancel')
        });

        it('should pass the tags to the addpatient modal', function() {
            spyOn($modal, 'open').and.callFake(function(){
                return {result: {then: function(fn){ fn('cancel') }}}
            });
            spyOn(modalInstance, 'close');
            $scope.newPatient({hospital_number: '555-123'});
            var resolvers = $modal.open.calls.mostRecent().args[0].resolve
            expect(resolvers.tags()).toEqual({})
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
                          "date_of_birth": "1999-12-12",
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
          expect(resolves.options()).toEqual(options);
          var expected_demographics = angular.copy(patientData.demographics[0]);
          expected_demographics.date_of_birth = "12/12/1999";
          expect(resolves.demographics()).toEqual(expected_demographics);
          expect(resolves.tags()).toEqual({});
      });

    });

});
