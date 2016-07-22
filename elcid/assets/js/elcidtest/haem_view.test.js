describe('HaemView', function() {
  "use strict";

  var controller;
  var $rootScope;
  var fakeEpisodes = [
    {
      id: 1,
      when: moment(new Date(2015, 1, 1)),
      created: moment(new Date(2014, 1, 1)),
    },
    {
      id: 2
    },
    {
      id: 3,
      created: moment(new Date(2014, 1, 1)),
    },
  ];

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
    it("should order clinical advice when then created by then undefined", function(){
      var ordered_events = _.sortBy(fakeEpisodes, function(x){
          return controller.clinicalAdviceOrdering(x);
      });

      expect(ordered_events[0].id).toBe(1);
      expect(ordered_events[1].id).toBe(3);
      expect(ordered_events[2].id).toBe(2);
    });
  });
});
