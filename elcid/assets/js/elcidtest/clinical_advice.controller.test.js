describe('ClinicalAdviceFormTest', function() {
    "use strict";

    var $scope, $httpBackend, $rootScope, $controller;
    var Episode;
    var mkcontroller;

    var episodedata = {
        demographics: [ { patient_id: 123 } ]
    }
    var recorddata = {
            'microbiology_input': {
                'name': 'microbiology_input',
                'fields': []
            }
    };

    beforeEach(function(){

        module('opal.controllers');

        inject(function($injector){
            $httpBackend = $injector.get('$httpBackend');
            $rootScope   = $injector.get('$rootScope');
            $scope       = $rootScope.$new();
            $controller  = $injector.get('$controller');
            Episode      = $injector.get('Episode');
        });

        $scope.episode = new Episode(episodedata);

        mkcontroller = function(){
            var ret = $controller('ClinicalAdviceForm', {
                $rootScope: $rootScope,
                $scope: $scope,
            });
        };
        $httpBackend.expectGET('/api/v0.1/userprofile/').respond({});
        $httpBackend.expectGET('/api/v0.1/record/').respond(recorddata);
    });

    describe('initialization', function() {

        it('should setup', function() {
            mkcontroller();
            $rootScope.$apply();
            $httpBackend.flush();
        });

    });

});
