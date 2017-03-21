describe('ResearchHospitalNumberCtrl', function (){
    "use strict";
    var $controller, $scope, $httpBackend, $modalInstance, $modal, $rootScope;
    var Item, Episode;
    var controller, options, schema, tags;

    beforeEach(module('opal.controllers', function($provide){
        $provide.service('Options', function(){
          return {
            then: function(x){ x({}); }
          };
        });
    }));

    beforeEach(inject(function($injector){
        $rootScope   = $injector.get('$rootScope');
        $scope       = $rootScope.$new();
        $modal       = $injector.get('$modal');
        $controller  = $injector.get('$controller');
        $httpBackend = $injector.get('$httpBackend');
        Episode      = $injector.get('Episode');
        Item         = $injector.get('Item');

        $modalInstance = $modal.open({template: 'Not a real template'});

        options = {};
        schema = {};

        controller = $controller('ResearchStudyHospitalNumberCtrl', {
            $scope        : $scope,
            $modalInstance: $modalInstance,
            $modal        : $modal,
            options       : options,
            schema        : schema,
        });

    }));

    it('should set up state', function(){
        expect($scope.model.hospitalNumber).toBe(null);
    });


    describe('newPatient()', function (){

        beforeEach(function(){
            spyOn($modal, 'open').and.callThrough();
            $httpBackend.whenGET('/templates/modals/add_episode_without_teams.html/').respond('hi');
            $httpBackend.expectGET('/api/v0.1/userprofile/').respond({});
            $httpBackend.expectGET('/api/v0.1/referencedata/').respond({});
        });

        it('Should call the AddEpisode controller', function () {
            $scope.newPatient({});
            var callArgs = $modal.open.calls.mostRecent().args;
            expect(callArgs[0].controller).toBe('AddEpisodeCtrl');
            $httpBackend.flush();
        });

        it('Should use the without teams template', function () {
            $scope.newPatient({});
            var callArgs = $modal.open.calls.mostRecent().args;
            expect(callArgs[0].templateUrl).toBe('/templates/modals/add_episode_without_teams.html/');
            $httpBackend.flush();
        });

        it('Should pass through hospital number', function () {
            var hospital_number = '12345';
            $scope.model.hospitalNumber = hospital_number;
            $scope.newPatient({});
            var callArgs = $modal.open.calls.mostRecent().args;
            expect(callArgs[0].resolve.demographics().hospital_number).toBe(hospital_number)
            $httpBackend.flush();
        });

    });

});
