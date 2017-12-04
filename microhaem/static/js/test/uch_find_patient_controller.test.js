describe('UchFindPatientCtrl', function() {
  "use strict";
  var scope, Episode, $controller, controller, $window;
  var $rootScope, opalTestHelper, Pathway;

  beforeEach(function(){
    module('opal.controllers');
    module('opal.services');
    module('opal.test');

    inject(function($injector){
      $rootScope = $injector.get('$rootScope');
      scope = $rootScope.$new();
      Episode = $injector.get('Episode');
      $controller = $injector.get('$controller');
      opalTestHelper = $injector.get('opalTestHelper');
      Pathway = $injector.get('Pathway');
    });


    $rootScope.fields = opalTestHelper.getRecordLoaderData();
    $window = {alert: jasmine.createSpy()};

    scope.pathway = new Pathway({
      save_url: "/some_url"
    });
    scope.editing = {};
    controller = $controller('UchFindPatientCtrl', {
      scope: scope,
      Episode: Episode,
      step: {},
      episode: {},
      $window: $window
    });
  });

  it("should initialise the scope", function(){
    var fakeScope = {};
    controller.initialise(fakeScope);
    expect(fakeScope.demographics.hospital_number).toBe(undefined);
    expect(fakeScope.state).toBe('initial');
    expect(fakeScope.hideFooter).toBe(true);
  });

  it("should change scope if we're unable to find a patient", function(){
    expect(scope.state).toBe('initial');
    scope.new_patient();
    expect(scope.state).toBe('editing_demographics');
    expect(scope.hideFooter).toBe(false);
  });

  it("should look up hospital numbers", function(){
    spyOn(Episode, "findByHospitalNumber");
    scope.demographics.hospital_number = "12";
    scope.lookup_hospital_number();
    var allCallArgs = Episode.findByHospitalNumber.calls.all();
    expect(allCallArgs.length).toBe(1);
    var callArgs = allCallArgs[0].args;
    expect(callArgs[0]).toBe("12");
    expect(callArgs[1].newPatient).toEqual(scope.new_patient);
    expect(callArgs[1].newForPatient).toEqual(scope.new_for_patient);
  });

  it("should throw an error if the hospital number isn't found", function(){
    spyOn(Episode, "findByHospitalNumber");
    scope.demographics.hospital_number = "12";
    scope.lookup_hospital_number();
    var allCallArgs = Episode.findByHospitalNumber.calls.all();
    expect(allCallArgs.length).toBe(1);
    var callArgs = allCallArgs[0].args;
    expect(callArgs[1].error());
    expect($window.alert).toHaveBeenCalledWith('ERROR: More than one patient found with hospital number');
  });

  it('should only show next if state is has_demographics or editing_demographics', function(){
    scope.state = "has_demographics";
    expect(scope.showNext()).toBe(true);
    scope.state = "editing_demographics";
    expect(scope.showNext()).toBe(true);
  });

  it('should only show next if state is neither has_demographics or editing_demographics', function(){
    scope.state = "something";
    expect(scope.showNext()).toBe(false);
  });

  it('should update the save_url if an patient is found with no open episode', function(){
    var patient = opalTestHelper.newPatient($rootScope);
    _.each(patient.episodes, function(e){
      e.end = new moment();
    });

    scope.new_for_patient(patient);
    expect(scope.pathway.save_url).toBe("/some_url/" + patient.id);
  });

  it('should update the save url if a patient with an open episode is found', function(){
    var patient = opalTestHelper.newPatient($rootScope);
    _.each(patient.episodes, function(e){
      e.end = undefined;
    });
    scope.new_for_patient(patient);
    expect(scope.pathway.save_url).toBe("/some_url/" + patient.id + "/123");
  });

  it('should update the editing dictionary if a patient with an open episode is found', function(){
    var patient = opalTestHelper.newPatient($rootScope);
    _.each(patient.episodes, function(e){
      e.end = null;
    });
    scope.new_for_patient(patient);
    expect(scope.state).toBe('has_demographics');
    expect(!!scope.editing.diagnosis.length).toBe(true);
  });

  it('should just update the demographics with only a demographics if no open episode is found', function(){
    var patient = opalTestHelper.newPatient($rootScope);
    scope.new_for_patient(patient);
    expect(scope.state).toBe('has_demographics');
    expect(
      scope.demographics.first_name).toBe(patient.demographics[0].first_name
    );
  });
});
