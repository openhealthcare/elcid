describe('ClinicalAdviceFormTest', function() {
  "use strict";

  var $scope, $httpBackend, $rootScope, $controller;
  var Episode, $cookies;
  var mkcontroller, mockReferenceDataLoader, recordLoader;

  var episodedata = {
    demographics: [ { patient_id: 123 } ]
  };

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

  beforeEach(function(){
    mockReferenceDataLoader = {load: function(){}}; // jasmine.createSpyObj(["load"])
    spyOn(mockReferenceDataLoader, "load").and.returnValue({
      then: function(someFun){
        return someFun(mockReferenceData);
      }
    });

    recordLoader = {load: function(){}}; // jasmine.createSpyObj(["load"])
    spyOn(recordLoader, "load").and.returnValue({
      then: function(someFun){
        return someFun(recorddata);
      }
    });


    module('opal.controllers');
    $cookies = jasmine.createSpyObj('$cookies', ['get', 'put']);
    $cookies.get.and.callFake(function(x){
        if(x === 'patientNotes-reasonForInteraction'){
          return 'issues'
        }
        else{
          return 'Dr Doctor'
        }
    });

    inject(function($injector){
      $httpBackend = $injector.get('$httpBackend');
      $rootScope   = $injector.get('$rootScope');
      $scope       = $rootScope.$new();
      $controller  = $injector.get('$controller');
      Episode      = $injector.get('Episode');
    });

    $scope.episode = new Episode(episodedata);
    $rootScope.fields = recorddata;

    mkcontroller = function(){
      return $controller('ClinicalAdviceForm', {
        $rootScope: $rootScope,
        $scope: $scope,
        Referencedata: mockReferenceDataLoader,
        $cookies: $cookies,
        recordLoader: recordLoader
      });
    };
  });

  afterEach(function(){
    $httpBackend.verifyNoOutstandingExpectation();
    $httpBackend.verifyNoOutstandingRequest();
  });

  describe('initialization', function() {
    it('should put look up lists on the scope', function(){
      var ctrl = mkcontroller();
      expect(ctrl.some_list).toEqual([]);
      expect(mockReferenceDataLoader.load).toHaveBeenCalled();
    });

    it('should populate editing with a microbiology_input record', function(){
      var ctrl = mkcontroller();
      expect(!!ctrl.editing).toBe(true);
      expect(ctrl.editing.reason_for_interaction).toBe('issues');
      expect(ctrl.editing.discussed_with).toBe('Dr Doctor');
      expect(recordLoader.load).toHaveBeenCalled();
    });

    it('should save items and store them to cookies', function(){
      var ctrl = mkcontroller();
      ctrl.editing.reason_for_interaction = "no issues";
      ctrl.editing.discussed_with = "Nurse Nurse";
      $httpBackend.expectPOST('/api/v0.1/microbiology_input/', ctrl.editing).respond({});
      ctrl.save();
      $httpBackend.flush();
      expect($cookies.put.calls.argsFor(0)).toEqual([
        'patientNotes-reasonForInteraction',
        "no issues"
      ]);
      expect($cookies.put.calls.argsFor(1)).toEqual([
        'patientNotes-discussedWith',
        "Nurse Nurse"
      ]);
    });
  });
});
