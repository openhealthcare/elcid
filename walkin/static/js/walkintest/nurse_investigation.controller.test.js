describe('WalkinNurseInvestigationsCtrl', function (){
    "use strict";

    var $controller, $scope, $modalInstance, $httpBackend, $rootScope, episode;
    var today, Episode, controller;

    beforeEach(module('opal.controllers'));

    beforeEach(inject(function($injector){
        today = moment();

        var $modal   = $injector.get('$modal');
        $rootScope   = $injector.get('$rootScope');
        $scope       = $rootScope.$new();
        $controller  = $injector.get('$controller');
        Episode      = $injector.get('Episode');
        $httpBackend = $injector.get('$httpBackend');

        $modalInstance = $modal.open({template: 'Not a real template'})
        episode = new Episode({demographics: [{patient_id: 1234}]});
        $rootScope.fields = {
            'microbiology_test': {
                name: 'microbiology_test',
                single: false,
                fields: [
                    { name: 'test', type: 'string' },
                    { name: 'date_ordered', type: 'date' }
                ]
            }
        }

        controller = $controller('WalkinNurseInvestigationsCtrl', {
            $scope         : $scope,
            $modalInstance : $modalInstance,
            episode        : episode
        });

        $httpBackend.expectGET('/api/v0.1/userprofile/').respond({});
    }));

    it('Should set up an investigations object', function () {
        expect($scope.investigations).toEqual({});
    });

    describe('with existing tests', function (){

        beforeEach(
            inject(function($injector){
                var episode = new Episode({demographics: [{patient_id: 1234}]});
                var test = episode.newItem('microbiology_test');
                test.test = 'Serum Save';
                episode.addItem(test);

                var controller = $controller('WalkinNurseInvestigationsCtrl', {
                    $scope         : $scope,
                    $modalInstance : $modalInstance,
                    episode        : episode
                });
            })

        );


        it('Should have positive investigations when they exist', function () {
            expect($scope.investigations.serum_save).toBe(true);
        });

        it('save() Should not add a second instance of the pre-existing test', function () {
            $scope.investigations.blood_culture = true;

            $httpBackend.expectPOST('/api/v0.1/microbiology_test/',
                                    {test: 'Blood Culture', date_ordered: today.format('DD/MM/YYYY')}).respond('yes');
            $scope.save();

            $httpBackend.flush();
        });

    });

    describe('save()', function (){

        it('Should create an investigation', function () {
            $scope.investigations.blood_culture = true;

            $httpBackend.expectPOST('/api/v0.1/microbiology_test/',
                                  {
                                      test: 'Blood Culture',
                                      date_ordered: today.format('DD/MM/YYYY')}).respond('yes');
            $scope.save();
            $httpBackend.flush();
        });

        it('Should create multiple investigations', function () {
            $scope.investigations.blood_culture = true;
            $scope.investigations.malaria_film  = true

            $httpBackend.expectPOST('/api/v0.1/microbiology_test/',
                                    {test: 'Blood Culture', date_ordered: today.format('DD/MM/YYYY')})
                .respond('yes');
            $httpBackend.expectPOST('/api/v0.1/microbiology_test/',
                                    {test: 'Malaria Film', date_ordered: today.format('DD/MM/YYYY')})
                .respond('yes');

            expect($scope.saving).toBe(false);
            $scope.save();
            expect($scope.saving).toBe(true);
            $httpBackend.flush();
            expect($scope.saving).toBe(false);
        });

        it('Should close the modal', function () {
            spyOn($modalInstance, 'close').and.returnValue(true);
            $scope.save();
            expect($modalInstance.close).toHaveBeenCalled();
        });
    });

    describe('cancel()', function (){
        it('Should close the modal', function () {
            spyOn($modalInstance, 'close').and.returnValue(true);
            $scope.cancel();
            expect($modalInstance.close).toHaveBeenCalledWith('cancel');
        });
    });

});
