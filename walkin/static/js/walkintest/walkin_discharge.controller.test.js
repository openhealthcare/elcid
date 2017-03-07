  describe('WalkinDischargeCtrl', function(){
    "use strict";

    var $controller, $scope, $modalInstance, $httpBackend, $rootScope, $modal, $q, growl;
    var Episode, episode, tags, modalResolved;
    var today = new Date();
    var today_string = moment(today).format('DD/MM/YYYY');

    var referencedata = {
        toLookuplists: function(){ return {"ward_list": ["1q"]}; }
    };
    var metadata = {"tags": ["someTags"]};

    beforeEach(module('opal.controllers'));

    beforeEach(inject(function($injector){

        $rootScope   = $injector.get('$rootScope');
        $scope       = $rootScope.$new();
        $modal       = $injector.get('$modal');
        $controller  = $injector.get('$controller');
        Episode      = $injector.get('Episode');
        $httpBackend = $injector.get('$httpBackend');
        $q           = $injector.get('$q');

        $modalInstance = $modal.open({template: 'Not a real template'});
        spyOn($modal, 'open').and.returnValue({
          result: {
            then: function(fn){
              modalResolved();
              fn();
            }
          }
        });
        tags = {};
        modalResolved = jasmine.createSpy();

        $rootScope.fields = {
            'walkin_nurse_led_care': {
                name:  'walkin_nurse_led_care',
                single: false,
                fields: [
                    { name: 'reason', type: 'string' },
                    { name: 'treatment', type: 'text' }
                ]
            },
            'tagging': {
                name: 'tagging',
                single: false,
                fields: [
                    { name: 'walkin', type: 'boolean' },
                    { name: 'walkin_triage', type: 'boolean' },
                    { name: 'walkin_doctor', type: 'boolean' },
                    { name: 'walkin_review', type: 'boolean' }
                ]
            },
            "management": {
                "fields": [
                    {
                        "lookup_list": null,
                        "type": "token",
                        "name": "consistency_token",
                        "title": "Consistency Token"
                    },
                    {
                        "lookup_list": null,
                        "type": "date",
                        "name": "date_of_appointment",
                        "title": "Date Of Appointment"
                    },
                    {
                        "lookup_list": null,
                        "type": "string",
                        "name": "advice",
                        "title": "Advice"
                    },
                    {
                        "lookup_list": null,
                        "type": "string",
                        "name": "results_actioned",
                        "title": "Results Actioned"
                    },
                    {
                        "lookup_list": "management_follow_up",
                        "type": "string",
                        "name": "follow_up",
                        "title": "Follow Up"
                    },
                    {
                        "lookup_list": "management_clinics",
                        "type": "string",
                        "name": "follow_up_clinic",
                        "title": "Follow Up Clinic"
                    }
                ],
                "single": false,
                "display_name": "Management",
                "name": "management"
            }
        }

        growl = {success: jasmine.createSpy('growl.success')};

        episode = new Episode(
            {id: 555, management: [{}], tagging: [{}],
             demographics: [{ patient_id: 1234 }]}
        );

        var controller = $controller('WalkinDischargeCtrl', {
            $scope         : $scope,
            $modalInstance : $modalInstance,
            growl          : growl,
            referencedata  : referencedata,
            metadata       : metadata,
            tags           : tags,
            episode        : episode,
        });
    }));

    describe('move_to_review()', function (){

        beforeEach(function(){
            $httpBackend.expectGET('/api/v0.1/userprofile/').respond({});
            $httpBackend.expectPUT(
                '/api/v0.1/episode/555/',
                {id: 555, discharge_date: today_string }).respond({});
            spyOn($modalInstance, 'close');
        });

        it('Should set a discharge date', function () {
            $httpBackend.expectPUT('/api/v0.1/tagging/555/').respond({});
            /// This is actually asserted by the PUT expectation for /episode/555 above
            $scope.move_to_review();
            $httpBackend.flush()
            $scope.$digest(); // Fire actual resolving
        });

        it('Should send a growl message', function () {
            $httpBackend.expectPUT('/api/v0.1/tagging/555/').respond({});
            $scope.move_to_review();
            $httpBackend.flush()
            $scope.$digest(); // Fire actual resolving
            expect(growl.success.calls.mostRecent().args[0])
                .toBe('Moved to Review list');
        });

        it('Should close the modal', function () {
            $httpBackend.expectPUT('/api/v0.1/tagging/555/').respond({});
            $scope.move_to_review();
            $httpBackend.flush()
            $scope.$digest(); // Fire actual resolving
            expect($modalInstance.close).toHaveBeenCalled();
        });

        it('Should update the tags', function () {
            $httpBackend.expectPUT(
                '/api/v0.1/tagging/555/',
                {id: 555, walkin_doctor: false, walkin_review: true}).respond({});
            $scope.move_to_review();
            $httpBackend.flush()
            $scope.$digest(); // Fire actual resolving
        });


    });

    describe('nurse_led_care()', function (){

        beforeEach(function(){
            $httpBackend.expectGET('/api/v0.1/userprofile/').respond({});
            $httpBackend.expectPOST('/api/v0.1/walkin_nurse_led_care/').respond({});
            $httpBackend.expectPOST('/api/v0.1/management/').respond({});
            $httpBackend.expectPUT('/api/v0.1/tagging/555/').respond({});
            $httpBackend.expectPUT(
                '/api/v0.1/episode/555/',
                {id: 555, discharge_date: today_string }).respond({});
        });

        it('Should save the discharge date', function () {
            spyOn($modalInstance, "close");
            episode.tagging = [{walkin_triage: true, walkin: true}];
            $scope.nurse_led_care();
            $httpBackend.flush();
            expect(modalResolved).toHaveBeenCalled();
            expect($modalInstance.close).toHaveBeenCalledWith('discharged');
        });

        it('Should save the discharge date', function () {
            spyOn($modalInstance, "close");
            $modal.open.and.returnValue({
              result: {
                then: function(successFn, failureFn){
                  failureFn();
                }
              }
            })
            episode.tagging = [{walkin_triage: true, walkin: true}];
            $scope.nurse_led_care();
            $httpBackend.flush();
            expect($modalInstance.close).toHaveBeenCalledWith('discharged');
        });
    });

    describe('remove_from_list()', function (){

        beforeEach(function(){
            $httpBackend.expectGET('/api/v0.1/userprofile/').respond({});
            $httpBackend.expectPUT(
                '/api/v0.1/tagging/555/', {
                    id: 555,
                    walkin_triage: false, walkin_doctor: false, walkin_review: false
            }).respond({});
            spyOn($modalInstance, 'close');
            spyOn($scope, 'cancel').and.callThrough();
        });

        it('Should set the discharge date if empty', function () {
            $httpBackend.expectPUT('/api/v0.1/episode/555/',
                                   {id: 555, discharge_date: today_string }).respond({});
            $scope.remove_from_list();
            $httpBackend.flush();
        });

        it('Should leave the existing date if set', function () {
            $scope.episode.discharge_date = Date(2014,1,1)
            $scope.remove_from_list();
            $httpBackend.flush();
        });

        it('Should send a growl success message', function () {
            $httpBackend.expectPUT('/api/v0.1/episode/555/').respond({});
            $scope.remove_from_list();
            $httpBackend.flush();
            expect(growl.success.calls.mostRecent().args[0])
                .toBe('Removed from Walk-in lists');
        });

        it('Should close the modal', function () {
            $httpBackend.expectPUT('/api/v0.1/episode/555/').respond({});
            $scope.remove_from_list();
            $httpBackend.flush();
            $scope.$digest(); // Fire actual resolving
            expect($modalInstance.close).toHaveBeenCalled();
        });

    });
    describe('set up', function(){
        it('should hoist reference data onto the scope', function(){
          expect($scope.ward_list).toEqual(["1q"]);
        });

        it('should hoise metadata onto the scope', function(){
          expect($scope.metadata).toEqual(metadata);
        });
    });

    describe('admit_to_ward()', function (){

        beforeEach(function(){
            $httpBackend.expectGET('/api/v0.1/userprofile/').respond({});
            $httpBackend.expectPOST('/episode/555/actions/copyto/Inpatient')
                .respond({id: 556, management: [{}], tagging: [{}],
                          demographics: [{patient_id: 1234}]});
            $httpBackend.expectPUT('/api/v0.1/tagging/555/').respond({});

            $httpBackend.expectPUT(
                '/api/v0.1/episode/555/',
                {id: 555, discharge_date: today_string }).respond({});
            $httpBackend.expectPUT('/api/v0.1/tagging/556/').respond({});
            $httpBackend.expectPOST('/api/v0.1/management/').respond({});
            spyOn($modalInstance, 'close');

        });

        it('Should set a discharge date', function () {
            /// This is actually asserted by the PUT expectation for /episode/555 above
            $scope.admit_to_ward();
            $httpBackend.flush()
            $scope.$digest(); // Fire actual resolving
        });

    });

});
