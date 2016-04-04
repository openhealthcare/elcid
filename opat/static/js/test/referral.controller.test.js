
describe('OPATReferralCtrl', function (){
    "use strict"

    var $controller, $scope, $httpBackend, $modalInstance, $modal;
    var $rootScope, Episode, Item, growl, fields;
    var controller;
    var columns = { default: [] };

    beforeEach(module('opal.controllers'));

    beforeEach(function(){
        inject(function($injector){
            $rootScope   = $injector.get('$rootScope');
            $scope       = $rootScope.$new();
            $modal       = $injector.get('$modal');
            $controller  = $injector.get('$controller');
            $httpBackend = $injector.get('$httpBackend');
            Episode      = $injector.get('Episode');
            Item         = $injector.get('Item');

            growl   = {success: jasmine.createSpy('Growl.success')};
            fields = {};
            _.each(columns.default, function(c){fields[c.name] = c; });
            $rootScope.fields = fields;

            $modalInstance = $modal.open({template: 'Not a real template'});

            controller = $controller('OPATReferralCtrl', {
                $scope        : $scope,
                $modalInstance: $modalInstance,
                growl         : growl,
                schema        : {},
                options       : {}
            });

        });
        $httpBackend.expectGET('/api/v0.1/userprofile/').respond({})
    });

    it('Should set up state', function () {
        expect($scope.model).toEqual({ hospital_number: null });
        expect($scope.patient).toBe(null);
        expect($scope.message).toBe(null);
    });

    describe('new_for_patient()', function (){
        var patient;

        beforeEach(function(){
            patient = {
                active_episode_id: 1,
                demographics: [{}],
                episodes: {
                    1: {
                        category: 'OPAT',
                        tagging: [{}],
                    }
                }
            };
        });

        describe('when a patient is on a list', function (){

            it('Should set the message', function () {
                patient.episodes[1].tagging[0].opat_referrals = true;
                $scope.new_for_patient(patient);
                var msg = 'Patient is already on the OPAT Referrals list';
                expect($scope.message).toEqual(msg)
            });

            describe('and has a previous opat episode that is not on a list', function() {

                it('Should set the message', function () {
                    patient.episodes[2] = angular.copy(patient.episodes[1]);
                    patient.episodes[2].tagging[0].opat_referrals = true;
                    $scope.new_for_patient(patient);
                    var msg = 'Patient is already on the OPAT Referrals list';
                    expect($scope.message).toEqual(msg)
                });

            });
        });

    });
});
