describe('DiagnosisAddEpisodeCtrl', function() {
    "use strict";

    var $rootScope, $scope, $modal, $httpBackend, $controller;
    var modalInstance, tags, options, demographics;

    demographics = {}
    tags = {tag: 'tropical', subtag: ''};
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
            expect($scope.currentSubTag).toEqual('');
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
