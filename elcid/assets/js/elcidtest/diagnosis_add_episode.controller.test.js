describe('DiagnosisAddEpisodeCtrl', function() {
    "use strict";

    var $rootScope, $scope, $modal, $httpBackend, $controller;
    var modalInstance, tags, options, demographics, tagServiceSpy;
    var mockTagService, tagServiceToSave;

    demographics = {patient_id: 1};
    tags = {tag: 'tropical', subtag: ''};


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
        tagServiceToSave = jasmine.createSpy('toSave').and.returnValue({"id_inpatients": true});
        mockTagService = jasmine.createSpy('TagService').and.returnValue(
            {toSave: tagServiceToSave}
        );
        // mockTagService.toSave = jasmine.createSpy('toSave');

        $controller('DiagnosisAddEpisodeCtrl', {
            $scope         : $scope,
            $modalInstance : modalInstance,
            options        : options,
            tags           : tags,
            demographics   : demographics,
            TagService: mockTagService,
            Episode: function(x){ return {
              newItem: function(){},
              presenting_complaint: [{}]
            };}
        });
    });

    describe('Freshly initialised', function() {
        it('should store the current tag and sub tag', function() {
            expect($scope.currentTag).toEqual('tropical');
            expect($scope.currentSubTag).toEqual('');
        });
    });

    describe('save', function(){
        it('should post on save', function(){
            spyOn($modal, "open").and.returnValue({
              result: {then: function(x){x(); } }
            });
            $scope.editing.date_of_admission = "10/02/2000";
            $scope.editing.demographics.date_of_birth = "10/02/1990";
            $scope.save();
            expect(tagServiceToSave).toHaveBeenCalled();
            $httpBackend.expectPOST('episode/', {
              "tagging":[{"id_inpatients": true}],
              "location":{"hospital":"UCLH"},
              "demographics":{
                "patient_id":1,
                "date_of_birth":"10/02/1990"
              },
              "date_of_admission": "10/02/2000",
            }).respond({demographics: [{patient_id: 1}]});
            $httpBackend.flush();
        });
    });
});
