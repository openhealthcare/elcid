describe('ClinicalAdviceFormTest', function() {
  "use strict";

  var $scope, $httpBackend, $rootScope, $controller;
  var Episode;
  var mkcontroller;

  var episodedata = {
    demographics: [ { patient_id: 123 } ]
  }
  var recorddata = {
    'microbiology_input': {
      'name': 'microbiology_input',
      'fields': []
    }
  };

  var mockReferenceData = {
    toLookuplists: function(){
      return {some_list: []};
    }
  };

  var mockReferenceDataLoader = {
    load: function(){
      return {
        then: function(someFun){
          return someFun(mockReferenceData);
        }
      };
    }
  };

  beforeEach(function(){

    module('opal.controllers');

    inject(function($injector){
      $httpBackend = $injector.get('$httpBackend');
      $rootScope   = $injector.get('$rootScope');
      $scope       = $rootScope.$new();
      $controller  = $injector.get('$controller');
      Episode      = $injector.get('Episode');
    });

    $scope.episode = new Episode(episodedata);

    mkcontroller = function(){
      return $controller('ClinicalAdviceForm', {
        $rootScope: $rootScope,
        $scope: $scope,
        Referencedata: mockReferenceDataLoader
      });
    };
    // $httpBackend.expectGET('/api/v0.1/userprofile/').respond({});
    $httpBackend.expectGET('/api/v0.1/record/').respond(recorddata);
  });

  afterEach(function(){
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  describe('initialization', function() {
    it('should put look up lists on the scope', function(){
      var ctrl = mkcontroller();
      $httpBackend.flush();
      expect(ctrl.some_list).toEqual([]);
    });

    it('should populate editing with a microbiology_input record', function(){
      var ctrl = mkcontroller();
      $rootScope.$apply();
      $httpBackend.flush();

      expect(!!ctrl.editing).toBe(true);
      expect(_.contains(_.keys(ctrl.editing), "reason_for_interaction")).toBe(true);
      expect(_.contains(_.keys(ctrl.editing), "discussed_with")).toBe(true);
    });
  });
});
