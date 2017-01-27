describe('TropicalLiasonAddPatient', function(){
  var $rootScope, $scope, $httpBackend, $modalInstance, $modal;
  var controller, $controller, Episode, item;

  beforeEach(function(){
    module('opal.controllers');
    inject(function($injector){
        $httpBackend = $injector.get('$httpBackend');
        $rootScope = $injector.get('$rootScope');
        $controller = $injector.get('$controller');
        $q = $injector.get('$q');
        $http = $injector.get('$http');
    });

    $modalInstance = {
      close: function(){}
    };

    FieldTranslater = {
      jsToPatient: function(){}
    };

    spyOn($modalInstance, "close");

    item = {save: function(){}};

    Episode = function(someArgs){
      _.extend(this, someArgs);
      this.newItem = function(){ return item; }
    };
    var FieldTranslater = {
      jsToPatient: function(someVars){ return someVars; }
    }

    $scope = $rootScope.$new();
    controller = $controller('TropicalLiasonAddPatient', {
        $scope : $scope,
        $modalInstance: $modalInstance,
        $q: $q,
        $http: $http,
        Episode: Episode,
        FieldTranslater: FieldTranslater
    });
  });

  it('should add tags to the scope', function(){
    expect($scope.editing.tagging.tropical_liason).toBe(true);
  });

  it('should save an episode, but not tropical liason if it doesnt exist', function(){
    $scope.editing.demographics = {
      first_name: "Pete"
    };
    var someEpisode = {};

    $httpBackend.expectPOST(
      '/api/v0.1/episode/',
      {
        category_name: "Tropical Liason",
        demographics: {first_name: "Pete"},
        tagging: {tropical_liason: true}
      }
    ).respond(someEpisode);

    $scope.save();

    $httpBackend.flush();
    expect($modalInstance.close).toHaveBeenCalled();

    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();

  });

  it('should save an episode and tropical liason if available', function(){
    $scope.editing.demographics = {
      first_name: "Pete"
    };

    $scope.editing.external_liason_contact_details = {
      external_hospital_number: "123"
    };
    var someEpisode = {};
    spyOn(item, "save").and.returnValue({then: function(fn){fn();}})

    $httpBackend.expectPOST(
      '/api/v0.1/episode/',
      {
        category_name: "Tropical Liason",
        demographics: {first_name: "Pete"},
        tagging: {tropical_liason: true}
      }
    ).respond(someEpisode);

    $scope.save();

    $httpBackend.flush();
    expect($modalInstance.close).toHaveBeenCalled();
    expect(item.save).toHaveBeenCalledWith($scope.editing.external_liason_contact_details)

    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

});
