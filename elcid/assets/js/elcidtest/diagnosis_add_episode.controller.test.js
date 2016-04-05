describe('DiagnosisAddEpisodeCtrl', function() {
    "use strict";

    var $rootScope, $scope, $modal, $httpBackend, $controller;
    var modalInstance, tags, options, demographics;

    var fields = {
        presenting_complaint: {
            name: 'presenting_complaint',
            fields: []
        }
    };

    demographics = { patient_id: 123 };
    tags = { tag: 'tropical', subtag: 'inpatients' };
    options = {
        'symptom_list': [
            'cough',
            'rash'
        ]
    };

    beforeEach(module('opal.controllers'));
    beforeEach(function(){
        inject(function($injector){
            $httpBackend    = $injector.get('$httpBackend');
            $rootScope      = $injector.get('$rootScope');
            $modal          = $injector.get('$modal');
            $controller = $injector.get('$controller');
        });

        $rootScope.fields = fields;

        $scope = $rootScope.$new();
        modalInstance = $modal.open({template: 'notatemplate'});

        $controller('DiagnosisAddEpisodeCtrl', {
            $scope         : $scope,
            $modalInstance : modalInstance,
            options        : options,
            tags           : tags,
            demographics   : demographics
        });
    });

    describe('Freshly initialised', function() {
        it('should store the current tag and sub tag', function() {
            expect($scope.currentTag).toEqual('tropical');
            expect($scope.currentSubTag).toEqual('inpatients');
        });
    });

    describe('save()', function() {

        it('should save the episode data', function() {
            $httpBackend.expectGET('/api/v0.1/userprofile/').respond({});
            var episodeData = {
                tagging     : [ { tropical: true, inpatients: true }],
                location    : { hospital: "UCLH" },
                demographics: { patient_id: 123 }
            };
            var responseData = angular.copy(episodeData);
            responseData.location = [responseData.location];
            responseData.demographics = [responseData.demographics]
            $httpBackend.expectPOST('episode/', episodeData).respond(responseData);
            $httpBackend.expectGET('/templates/modals/presenting_complaint.html/').respond('notarealtemplate');

            $scope.save();

            $rootScope.$apply();
            $httpBackend.flush();
        });

    });

    describe('cancel()', function(){

        it('should close with null', function(){
            spyOn(modalInstance, 'close');
            $scope.cancel();
            expect(modalInstance.close).toHaveBeenCalledWith(null);
        });

    });

});
