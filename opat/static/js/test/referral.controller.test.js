
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
            spyOn($modalInstance, "close");

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

    describe('newForPatient()', function (){
        var patient;

        beforeEach(function(){
            patient = {
                active_episode_id: 1,
                demographics: [{}],
                episodes: {
                    1: {
                        category_name: 'OPAT',
                        tagging: [{}],
                    }
                }
            };
        });

        describe('When a patient is on a list', function (){
            it('Should set the message if its currently on a list', function () {
                patient.episodes[1].tagging[0].opat_referrals = true;
                $scope.newForPatient(patient);
                var msg = 'Patient is already on the OPAT Referrals list';
                expect($scope.message).toEqual(msg)
            });

            it('Should set the message if it was previously on a list', function () {
                patient.episodes[2] = angular.copy(patient.episodes[1]);
                patient.episodes[2].tagging[0].opat_referrals = true;
                $scope.newForPatient(patient);
                var msg = 'Patient is already on the OPAT Referrals list';
                expect($scope.message).toEqual(msg)
            });
        });

        describe('A patient who has an active episode but is not currently on a list', function(){
            it('should call make_an_episode_from_previous_episode', function(){
                spyOn($scope, "make_an_episode_from_previous_episode");
                $scope.newForPatient(patient);
                expect($scope.make_an_episode_from_previous_episode).toHaveBeenCalled();
            });
        });

        describe('A patient who does not currently have an active episode', function(){
            it('should call add_for_patient if they do not have a previous episode', function(){
                patient.active_episode_id = null;
                spyOn($scope, "add_for_patient");
                $scope.newForPatient(patient);
                expect($scope.add_for_patient).toHaveBeenCalled();
            });
        });
    });
});
