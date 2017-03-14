describe('DiagnosisDischarge', function() {
    "use strict";

    var $rootScope, $scope, $modal, $httpBackend, $controller;
    var Episode, $q, DischargePatientService, dischargePatientService;
    var modalInstance, tags, episode, fieldData, growl;

    var referencedata = {toLookuplists: function(){ return {}; }};

    fieldData = {
        'demographics': {
            name: 'demographics',
            fields: []
        },
        location: {
            name: 'location',
            fields: []
        },
        presenting_complaint: {
            name: 'presenting_complaint',
            fields: []
        },
        antimicrobial: {
            name: 'antimicrobial',
            fields: []
        },
        travel: {
            name: 'travel',
            fields: []
        },
        primary_diagnosis: {
            name: 'primary_diagnosis',
            fields: []
        },
        consultant_at_discharge: {
            name: 'consultant_at_discharge',
            fields: []
        },
        secondary_diagnosis: {
            name: 'secondary_diagnosis',
            fields: []
        }
    };

    beforeEach(module('opal.controllers'));

    beforeEach(function(){
        inject(function($injector){
            $httpBackend = $injector.get('$httpBackend');
            $rootScope   = $injector.get('$rootScope');
            $modal       = $injector.get('$modal');
            $controller  = $injector.get('$controller');
            Episode      = $injector.get('Episode');
        });

        $rootScope.fields = fieldData
        $scope = $rootScope.$new();
        $q = {
          all: function(){
            return {
              then: function(fn){
                fn();
              }
            }
          }
        }

        spyOn($q, "all").and.callThrough();

        episode = new Episode({
            demographics: [ { patient_id: 123} ],
            location: [ { category: 'first' } ],
            presenting_complaint: [],
            antimicrobial: [],
            travel: [],
            primary_diagnosis: [{condition: 'liver disease'}],
            consultant_at_discharge: [{consultant: 'Dr Foster'}],
            secondary_diagnosis: []
        });

        dischargePatientService = {
          getEditing: function(){ return {some: "editing"}; },
          discharge: function(){
            return {
              then: function(fn){fn();}
            };
          }
        };
        spyOn(dischargePatientService, "getEditing").and.callThrough();
        spyOn(dischargePatientService, "discharge").and.callThrough();

        var DischargePatientService = function(){};
        DischargePatientService.prototype = dischargePatientService;
        growl = jasmine.createSpyObj(["success"]);
        modalInstance = jasmine.createSpyObj(["close"]);

        $controller('DiagnosisDischargeCtrl', {
            $scope         : $scope,
            $modalInstance : modalInstance,
            referencedata  : referencedata,
            tags           : tags,
            episode        : episode,
            growl          : growl,
            $q             : $q,
            DischargePatientService: DischargePatientService
        });
    });

    describe('nextStep()', function() {

        it('should give you the next step', function() {
            expect($scope.nextStep()).toEqual('diagnosis');
        });

        it('should give you null on the last step', function() {
            $scope.step = 'discharge';
            expect($scope.nextStep()).toEqual(null);
        });

    });

    describe('previousStep()', function() {

        it('should return null on the first step', function() {
            expect($scope.previousStep()).toEqual(null)
        });

        it('should return the previous step', function() {
            $scope.step = 'discharge';
            expect($scope.previousStep()).toEqual('travel');
        });

    });

    describe('resetFormValidation()', function() {

        it('should reset the warning', function() {
            var form = {};
            $scope.resetFormValidation(form);
            expect(form.warning).toEqual(false);
        });

    });

    describe('resetRequired', function() {

        it('should reset the validity', function() {
            var formfield = { '$setValidity': jasmine.createSpy() };
            $scope.resetRequired(formfield);
            expect(formfield.$setValidity).toHaveBeenCalledWith('required', true)
        });

    });

    describe('processSteps', function(){
        it('should set the processSteps attribute', function(){
           expect(!!$scope.processSteps.length).toBe(true);
           _.each($scope.processSteps, function(step){
             expect(!!step.display_name).toBe(true);
             expect(!!step.icon).toBe(true);
           });
        });
    });

    describe('goToNextStep()', function() {
        var form, model;

        beforeEach(function(){
            form = {};
            model = {};
        });

        describe('diagnosis', function() {

            it('should not allow invlaid steps', function() {
                $scope.step = 'diagnosis';
                form.primary_diagnosis_condition = {
                    '$valid': false,
                    '$setDirty': jasmine.createSpy()
                };
                $scope.goToNextStep(form, model);
                expect(form.primary_diagnosis_condition.$setDirty).toHaveBeenCalledWith();
            });
        });

        describe('presenting_complaint', function() {
            it('should not allow invalid forms', function() {
                model.presenting_complaint = {symptoms: []};
                form.presenting_complaint_symptoms = {
                    '$setValidity': jasmine.createSpy(),
                    '$setDirty'   : jasmine.createSpy()
                };
                $scope.goToNextStep(form, model);
                expect(form.presenting_complaint_symptoms.$setValidity).toHaveBeenCalledWith("required", false);
                expect(form.presenting_complaint_symptoms.$setDirty).toHaveBeenCalledWith();
            });
        });

    });

    describe('save', function(){
      it('should close out with followup if category is followup', function(){
        $scope.editing.category = "Followup";
        $scope.save();
        expect(dischargePatientService.discharge).toHaveBeenCalled();
        expect($q.all).toHaveBeenCalled();
        expect(modalInstance.close).toHaveBeenCalledWith('followup');
      });

      it('should close out with discharge if category is not followup', function(){
        $scope.editing.category = "Discharged";
        $scope.save();
        expect(dischargePatientService.discharge).toHaveBeenCalled();
        expect($q.all).toHaveBeenCalled();
        expect(modalInstance.close).toHaveBeenCalledWith('discharged');
      });
    });

    describe('cancel()', function(){

        it('should close with null', function(){
            $scope.cancel();
            expect(modalInstance.close).toHaveBeenCalledWith('cancel');
        });

    });

});
