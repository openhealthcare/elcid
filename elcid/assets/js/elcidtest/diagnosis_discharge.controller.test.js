describe('DiagnosisDischarge', function() {
    "use strict";

    var $rootScope, $scope, $modal, $httpBackend, $controller;
    var Episode;
    var modalInstance, tags, options, episode, fieldData;

    fieldData = {
        'demographics': {
            name: 'demographics',
            fields: []
        },
        location: {
            name: 'location',
            fields: []
        },
        presenting_complaint: {
            name: 'presenting_complaint',
            fields: []
        },
        antimicrobial: {
            name: 'antimicrobial',
            fields: []
        },
        travel: {
            name: 'travel',
            fields: []
        },
        primary_diagnosis: {
            name: 'primary_diagnosis',
            fields: []
        },
        consultant_at_discharge: {
            name: 'consultant_at_discharge',
            fields: []
        },
        secondary_diagnosis: {
            name: 'secondary_diagnosis',
            fields: []
        }
    };

    beforeEach(module('opal.controllers'));

    beforeEach(function(){
        inject(function($injector){
            $httpBackend = $injector.get('$httpBackend');
            $rootScope   = $injector.get('$rootScope');
            $modal       = $injector.get('$modal');
            $controller  = $injector.get('$controller');
            Episode      = $injector.get('Episode');
        });

        $rootScope.fields = fieldData
        $scope = $rootScope.$new();
        modalInstance = $modal.open({template: 'notatemplate'});

        episode = new Episode({
            demographics: [ { patient_id: 123} ],
            location: [ { category: 'first' } ],
            presenting_complaint: [],
            antimicrobial: [],
            travel: [],
            primary_diagnosis: [{condition: 'liver disease'}],
            consultant_at_discharge: [{consultant: 'Dr Foster'}],
            secondary_diagnosis: []
        });

        $controller('DiagnosisDischargeCtrl', {
            $scope         : $scope,
            $modalInstance : modalInstance,
            options        : options,
            tags           : tags,
            episode        : episode
        });
    });


    describe('cancel()', function(){

        it('should close with null', function(){
            spyOn(modalInstance, 'close');
            $scope.cancel();
            expect(modalInstance.close).toHaveBeenCalledWith('cancel');
        });

    });

});
