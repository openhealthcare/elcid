describe('DiagnosisHospitalNumber', function(){
    "use strict";

    var $rootScope, $scope, $modal, $httpBackend, $controller;
    var modalInstance, tags, options, hospital_number;

    tags = {}

    beforeEach(module('opal.controllers'));
    beforeEach(function(){
        inject(function($injector){
            $httpBackend    = $injector.get('$httpBackend');
            $rootScope      = $injector.get('$rootScope');
            $modal          = $injector.get('$modal');
            $controller = $injector.get('$controller');
        });

        $scope = $rootScope.$new();
        modalInstance = $modal.open({template: 'notatemplate'});

        $controller('DiagnosisHospitalNumberCtrl', {
            $scope         : $scope,
            $modalInstance : modalInstance,
            options        : options,
            tags           : tags,
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
            expect(resolvers.tags()).toEqual(tags)
        });
    });

});
