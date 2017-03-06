describe('ClinicalAdviceFormTest', function() {
  "use strict";

  var $scope, $httpBackend, $rootScope, $controller;
  var Episode, $cookies;
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
      return {some_list: []}
    }
  };

  var mockReferenceDataPromise = {
    then: function(someFun){
      return someFun(mockReferenceData);
    }
  }

  beforeEach(function(){

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

    mkcontroller = function(){
      return $controller('ClinicalAdviceForm', {
        $rootScope: $rootScope,
        $scope: $scope,
        Referencedata: mockReferenceDataPromise,
        $cookies: $cookies
      });
    };
    $httpBackend.expectGET('/api/v0.1/userprofile/').respond({});
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
      expect(ctrl.editing.reason_for_interaction).toBe('issues');
      expect(ctrl.editing.discussed_with).toBe('Dr Doctor');
    });

    it('should save items and store them to cookies', function(){
      var ctrl = mkcontroller();
      $rootScope.$apply();
      $httpBackend.flush();
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
