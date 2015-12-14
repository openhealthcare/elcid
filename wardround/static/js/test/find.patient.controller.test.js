describe('WardRoundFindPatientCtrl', function (){
    "use strict";

    var $scope, $httpBackend, $modalInstance;
    var Episode, $rootScope, episodes, controller;
    var demographics1, demographics2;

    beforeEach(module('opal.wardround.controllers'));

    beforeEach(inject(function($injector){
        var $rootScope   = $injector.get('$rootScope');
        var $controller  = $injector.get('$controller');
        var $modal       = $injector.get('$modal');
        $scope       = $rootScope.$new();
        Episode      = $injector.get('Episode');
        $httpBackend = $injector.get('$httpBackend');

        $modalInstance = $modal.open({template: 'Not a real template'});
        demographics1 = {name: 'Amy Andrews', hospital_number: '1111'};
        demographics2 = {name: 'Brenda Benson', hospital_number: '2222'};
        episodes = [
            new Episode({demographics: [demographics1]}),
            new Episode({demographics: [demographics2]}),
        ];

        controller = $controller('WardRoundFindPatientCtrl', {
            $scope        : $scope,
            $modalInstance: $modalInstance,
            episodes      : episodes,
        });
    }));

    afterEach(function() {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
    });

    describe('get_filtered_episodes()', function (){

        it('Should allow all episodes when the query is ""', function () {
            expect($scope.filter.query).toBe("");
            expect($scope.get_filtered_episodes()).toEqual($scope.episodes);
        });

        it('Should filter on hospital number', function () {
            $scope.filter.query = '1111';
            expect($scope.get_filtered_episodes()).toEqual([$scope.episodes[0]]);
        });

        it('Should filter on name', function () {
            $scope.filter.query = 'Benson';
            expect($scope.get_filtered_episodes()).toEqual([$scope.episodes[1]]);
        });

        it('Should filter on name case insensitively', function () {
            $scope.filter.query = 'benson';
            expect($scope.get_filtered_episodes()).toEqual([$scope.episodes[1]]);
        });

        it('Should filter out episodes without demographics', function () {
            $scope.episodes.push(new Episode({}));
            expect($scope.get_filtered_episodes()).toEqual([$scope.episodes[0],
                                                           $scope.episodes[1]]);
        });
    });

});
