describe('DiagnosisAddEpisodeCtrl', function() {
    "use strict";

    var $rootScope, $scope, $modal, $httpBackend, $controller;
    var modalInstance, tags, demographics;
    var mockTagService;


    var fields = {
        presenting_complaint: {
            name: 'presenting_complaint',
            fields: []
        }
    };

    demographics = { patient_id: 123 };
    tags = { tag: 'tropical', subtag: 'inpatients' };
    var referencedata = {
        'symptom_list': [
            'cough',
            'rash'
        ]
    };
    referencedata.toLookuplists = function(){
        return referencedata
    }

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
            referencedata  : referencedata,
            tags           : tags,
            demographics   : demographics,
            Episode: function(x){ return {
              newItem: function(){},
              presenting_complaint: [{}],
            };}
        });
    });

    describe('cancel()', function(){

        it('should close with null', function(){
            spyOn(modalInstance, 'close');
            $scope.cancel();
            expect(modalInstance.close).toHaveBeenCalledWith(null);
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
            $httpBackend.expectPOST('/api/v0.1/episode/', {
              "tagging":{inpatients: true, tropical: true},
              "location":{"hospital":"UCH"},
              "demographics":{
                "patient_id":123,
                "date_of_birth":"10/02/1990"
              },
              "date_of_admission": "10/02/2000",
            }).respond({demographics: [{patient_id: 1}]});
            $httpBackend.flush();
        });
    });
});
