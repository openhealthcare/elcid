describe('OPATDischargeCtrl', function (){
    "use strict"
    var $controller, $scope, $httpBackend, $modalInstance, $modal;
    var Episode, Item, $rootScope, fields, episodeData;
    var controller, growl, columns;
    var episode, referencedata, tags;

    var columns = {
        "default": [
            {
                name: 'demographics',
                single: true,
                fields: [
                    {name: 'name', type: 'string'},
                    {name: 'date_of_birth', type: 'date'},
                ]},
            {
                name: 'location',
                single: true,
                fields: [
                    {name: 'category_name', type: 'string'},
                    {name: 'hospital', type: 'string'},
                    {name: 'ward', type: 'string'},
                    {name: 'bed', type: 'string'},
                    {name: 'date_of_admission', type: 'date'},
                    {name: 'tags', type: 'list'},
                ]},
            {
                name: 'diagnosis',
                single: false,
                fields: [
                    {name: 'condition', type: 'string'},
                    {name: 'provisional', type: 'boolean'},
                ]},
            {
                name: 'tagging',
                single: true,
                fields: [
                    { name: 'mine', type: 'boolean' }
                ]
            },
            {
                name: 'opat_meta',
                single: false,
                fields: [
                    { name: 'review_date', type: 'date' },
                    { name: 'reason_for_stopping', type: 'string' },
                    { name: 'unplanned_stop_reason', type: 'string' },
                    { name: 'stopping_iv_details', type: 'string' },
                    { name: 'treatment_outcome', type: 'string' },
                    { name: 'deceased', type: 'boolean' },
                    { name: 'death_category', type: 'string' },
                    { name: 'cause_of_death', type: 'string' },
                    { name: 'readmitted', type: 'boolean' },
                    { name: 'readmission_cause', type: 'string' },
                    { name: 'notes', type: 'text' },
                ]
            },
            {
                name  : 'opat_outcome',
                single: false,
                fields: [
                ]
            }

        ]
    };

    beforeEach(module('opal.controllers'));

    beforeEach(function(){
        inject(function($injector){
            $rootScope   = $injector.get('$rootScope');
            $scope       = $rootScope.$new();
            $modal       = $injector.get('$modal');
            $controller  = $injector.get('$controller');
            $httpBackend = $injector.get('$httpBackend');
            Episode      = $injector.get('Episode');
            Item         = $injector.get('Item');

            fields = {}
            _.each(columns.default, function(c){fields[c.name] = c});
            $rootScope.fields = fields;

            $modalInstance = $modal.open({template: 'Not a real template'});
            episodeData = {id: 33, tagging: [{opat: true}], demographics: [{patient_id: 20}]}
            episode = new Episode(episodeData);
            referencedata = { toLookuplists: function(){ return {} }};
            tags    = {};
            growl   = {success: jasmine.createSpy('Growl.success')}

            controller = $controller('OPATDischargeCtrl', {
                $scope        : $scope,
                $modalInstance: $modalInstance,
                episode       : episode,
                referencedata : referencedata,
                tags          : tags,
                growl         : growl
            });

        });
        $httpBackend.expectGET('/api/v0.1/userprofile/').respond({})

    });

    afterEach(function() {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
    });

    it('Should set up state', function () {
        expect($scope.episode).toBe(episode);
        $httpBackend.flush();
    });


    describe('completed_therapy()', function (){
        var metavars;

        beforeEach(function(){
            metavars = {
                review_date   : '22/12/1999',
                outcome       : 'death',
                died          : true,
                cause_of_death: 'negligence',
                death_category: 'preventable',
                readmitted    : false,
                notes         : 'whoops',
                infective_diagnosis: "Aspergillosis"
            };
            $scope.meta = metavars;
            var meta2 = angular.copy(metavars);
            meta2.episode_id = 33;
            meta2.review_date = '22/12/1999';
            meta2.treatment_outcome = 'death';
            meta2.deceased = true;
            delete meta2['outcome'];
            delete meta2['died'];
            delete meta2['infective_diagnosis'];

            // Should save the metadata
            $httpBackend.expectPOST('/api/v0.1/opat_meta/', meta2).respond({});
            // Should update the teams
            var taggingdata = {opat_current: false, opat_followup: false, id: 33}
            $httpBackend.expectPUT('/api/v0.1/tagging/33/', taggingdata).respond({});
            // Should set the discharge date
            var episode_data = {
                discharge_date: moment().format('DD/MM/YYYY'),
                id: 33
            }

            var expectedPost = {
              patient_outcome: undefined,
              outcome_stage: 'Completed Therapy',
              infective_diagnosis: metavars.infective_diagnosis,
              episode_id: 33
            };
            $httpBackend.expectPUT('/api/v0.1/episode/33/', episode_data).respond(episodeData);
            $httpBackend.expectPOST('/api/v0.1/opat_outcome/', expectedPost).respond({});
        });

        it('Should close the mdoal', function () {
            spyOn($modalInstance, 'close');
            $scope.completed_therapy();
            $httpBackend.flush();
            expect($modalInstance.close).toHaveBeenCalledWith('discharged');
        });


        it('Should send a growl message', function () {
            $scope.completed_therapy();
            $httpBackend.flush();
            expect(growl.success).toHaveBeenCalled();
        });
    });

    describe('switch_to_oral()', function(){

        beforeEach(function(){
            $httpBackend.expectPOST('/api/v0.1/opat_outcome/').respond({});
            $httpBackend.expectPOST('/api/v0.1/opat_meta/').respond({});
            $httpBackend.expectPUT('/api/v0.1/tagging/33/').respond({});
        });

        it('should send a growl message', function(){
            $scope.switch_to_oral();
            $httpBackend.flush();
            expect(growl.success).toHaveBeenCalled();
        })
    });

});
