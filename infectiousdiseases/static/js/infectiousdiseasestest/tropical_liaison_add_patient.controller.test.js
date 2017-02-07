describe('TropicalLiaisonAddPatient', function(){
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
    controller = $controller('TropicalLiaisonAddPatient', {
        $scope : $scope,
        $modalInstance: $modalInstance,
        $q: $q,
        $http: $http,
        Episode: Episode,
        FieldTranslater: FieldTranslater
    });
  });

  it('should add tags to the scope', function(){
    expect($scope.editing.tagging.tropical_liaison).toBe(true);
  });

  it('should save an episode, but not tropical liaison if it doesnt exist', function(){
    $scope.editing.demographics = {
      first_name: "Pete"
    };
    var someEpisode = {external_liaison_contact_details: [{id: 1}]};

    $httpBackend.expectPOST(
      '/api/v0.1/episode/',
      {
        category_name: "Tropical Liaison",
        demographics: {first_name: "Pete"},
        tagging: {tropical_liaison: true}
      }
    ).respond(someEpisode);

    $scope.save();

    $httpBackend.flush();
    expect($modalInstance.close).toHaveBeenCalled();

    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();

  });

  it('should save an episode and tropical liaison if available', function(){
    $scope.editing.demographics = {
      first_name: "Pete"
    };

    $scope.editing.external_liaison_contact_details = {
      external_hospital_number: "123"
    };
    var liaison = {id: 1, save: function(){}}
    var someEpisode = {external_liaison_contact_details: [liaison]};
    spyOn(liaison, "save").and.returnValue({then: function(fn){fn();}})

    $httpBackend.expectPOST(
      '/api/v0.1/episode/',
      {
        category_name: "Tropical Liaison",
        demographics: {first_name: "Pete"},
        tagging: {tropical_liaison: true}
      }
    ).respond(someEpisode);

    $scope.save();

    $httpBackend.flush();
    expect($modalInstance.close).toHaveBeenCalled();
    expect(liaison.save).toHaveBeenCalledWith($scope.editing.external_liaison_contact_details)

    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

});
