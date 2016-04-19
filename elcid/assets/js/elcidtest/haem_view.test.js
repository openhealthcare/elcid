describe('HaemView', function() {
  "use strict";

  var controller;
  var $rootScope;

  beforeEach(function(){
      var $controller;
      module('opal.controllers');
      inject(function($injector){
          $controller = $injector.get('$controller');
          $rootScope = $injector.get('$rootScope');
      });

      var $scope = $rootScope.$new();
      $scope.patient = {episodes: []};
      controller = $controller('HaemView', {$scope: $scope});
  });

  describe("it should order an event based on an episode date hierachy", function(){
      it("should use discharge_date as the higest priority", function(){
          var fakeEpisode = {
              discharge_date: moment(new Date(2015, 1, 1)),
              date_of_episode: moment(new Date(2014, 1, 1)),
              date_of_admission: moment(new Date(2013, 1, 1)),
          };
          var ordering = controller.getEpisodeOrdering(fakeEpisode);
          expect(ordering).toBe(-1422748800);
      });

      it("should use date_of_admission if no other date is available", function(){
        var fakeEpisode = {
            date_of_admission: moment(new Date(2015, 1, 1)),
        };
        var ordering = controller.getEpisodeOrdering(fakeEpisode);
        expect(ordering).toBe(-1422748800);
      });
  });
});
