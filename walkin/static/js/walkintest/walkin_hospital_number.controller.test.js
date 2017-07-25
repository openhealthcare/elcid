describe('WalkinHospitalNumberCtrl', function (){
    "use strict";
    var $controller, $scope, $modalInstance, $httpBackend, $rootScope, $modal;
    var schema, options, tags, Episode;

    tags = {tag: 'walkin', subtag: 'walkin_doctor'}

    beforeEach(module('opal.controllers'));

    beforeEach(inject(function($injector){
        $rootScope   = $injector.get('$rootScope');
        $scope       = $rootScope.$new();
        $controller  = $injector.get('$controller');
        $modal       = $injector.get('$modal');
        Episode      = $injector.get('Episode');
        $httpBackend = $injector.get('$httpBackend');

        $modalInstance = $modal.open({template: 'Not a real template'})
        spyOn($modalInstance, 'close');
        schema = {}
        options = {}

        $rootScope.fields = {
            'microbiology_test': {
                name: 'microbiology_test',
                single: false,
                fields: [
                    { name: 'test', type: 'string' },
                    { name: 'date_ordered', type: 'date' }
                ]
            },
            'management': {
                name: 'management',
                single: false,
                fields : [
                    { name: 'date_of_appointment', type: 'date' }
                ]
            },
            'demographics':{
                name: 'demographics',
                single: true,
                fields: [
                    { name: 'patient_id', type: 'string'}
                ]
            }

        }

        var controller = $controller('WalkinHospitalNumberCtrl', {
            $scope         : $scope,
            $modalInstance : $modalInstance,
            $modal         : $modal,
            schema         : schema,
            options        : options,
            tags           : tags
        });
    }));

    describe('tag_and_close()', function (){

        it('Should save and close', function () {
            var episode  = {
                id: '3',
                start: moment().format('YYYY-MM-DD'),
                end: moment().format('YYYY-MM-DD'),
                category: 'Walkin',
                demographics: [{patient_id: 123}]
            };
            $httpBackend.expectPUT('/api/v0.1/episode/3/').respond(episode);

            var test = {test: 'HIV Point of Care', episode_id: "3"};
            $httpBackend.expectPOST('/api/v0.1/microbiology_test/', test).respond(test);
            $scope.tag_and_close(episode);
            $httpBackend.flush();

            expect($modalInstance.close).toHaveBeenCalled();
        });

    });

    describe('newPatient()', function() {
        it('should pass through the tags', function() {
            spyOn($modal, 'open').and.callThrough();
            $scope.newPatient();
            var resolves = $modal.open.calls.mostRecent().args[0].resolve;
            expect(resolves.tags()).toEqual(tags);
            expect($modalInstance.close).not.toHaveBeenCalled();
        });

        it('Should resolve reference data', function(){
          spyOn($modal, 'open').and.callThrough();
          $scope.newPatient();
          var resolves = $modal.open.calls.mostRecent().args[0].resolve;
          var referenceDataLoader = jasmine.createSpyObj(["load"]);
          var referenceData = {"expected": "something"};
          referenceDataLoader.load.and.returnValue(referenceData);
          expect(resolves.referencedata(referenceDataLoader)).toBe(referenceData);
        });
    });

    describe('add_for_patient()', function() {

        it('should pass through the tags', function() {
            var patientData = {demographics: [{}]};
            spyOn($modal, 'open').and.callThrough();
            $scope.add_for_patient(patientData);
            var resolves = $modal.open.calls.mostRecent().args[0].resolve;
            expect(resolves.tags()).toEqual(tags);
        });

    });


});
