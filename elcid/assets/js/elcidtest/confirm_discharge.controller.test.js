describe('ConfirmDischargeCtrl', function(){
    "use strict";

    var $rootScope, $scope, $modal, $httpBackend, $controller;
    var modalInstance, tags, hospital_number, $q;

    beforeEach(module('opal.controllers'));

    beforeEach(function(){
        inject(function($injector){
            $scope = $injector.get('$scope');
            $modal = $injector.get('$modal');
            DischargePatientService = $injector.get('DischargePatientService');
            $controller = $injector.get('$controller');
        });

        $scope = $rootScope.$new();
        modalInstance = $modal.open({template: 'notatemplate'});

        $controller('ConfirmDischargeCtrl', {
            $scope         : $scope,
            $modalInstance : modalInstance,
            hospital_number: hospital_number,
            context: {ctx: 'some context'},
            patient: {},
            episode: {},
            tags: {someTag: 'or other'},
            context: {"some context": "useful"}
        });
    });

    it('should open the next modal with the controller passed in', function(){

    });

    it('')

});
