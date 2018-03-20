describe('OPATDischargeCtrl', function (){
    "use strict"
    var $controller, $scope, $httpBackend, $modalInstance, $modal;
    var Episode, Item, $rootScope, fields, episodeData;
    var controller, growl, columns, opalTestHelper;
    var episode, referencedata, tags;

    var columns = {
      opat_meta: {
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
      opat_outcome: {
          name  : 'opat_outcome',
          single: false,
          fields: []
      },

      opat_rejection: {
          name  : 'opat_outcome',
          single: false,
          fields: [
            { name: 'date', type: 'date' },
            { name: 'patient_choice', type: 'null_boolean' },
          ],
      },
      location: {
          name: 'location',
          single: true,
          fields: [
            { name: 'opat_acceptance', type: 'date' }
          ],
      }
    };

    beforeEach(module('opal.controllers'));

    beforeEach(function(){
        module('opal.controllers');
        module('opal.test');

        inject(function($injector){
            $rootScope   = $injector.get('$rootScope');
            $scope       = $rootScope.$new();
            $modal       = $injector.get('$modal');
            $controller  = $injector.get('$controller');
            $httpBackend = $injector.get('$httpBackend');
            Episode      = $injector.get('Episode');
            Item         = $injector.get('Item');
            opalTestHelper = $injector.get('opalTestHelper');
            var fields = opalTestHelper.getRecordLoaderData();
            _.extend(fields, columns);
            $rootScope.fields = fields;
            $modalInstance = $modal.open({template: 'Not a real template'});
            episodeData = {
              id: 33,
              tagging: [{opat: true}],
              demographics: [{patient_id: 20}],
              location: [{id: 1}]
            };
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
    });

    afterEach(function() {
        $httpBackend.verifyNoOutstandingExpectation();
        $httpBackend.verifyNoOutstandingRequest();
    });

    it('Should set up state', function () {
        expect($scope.episode).toBe(episode);
    });

    describe('reject', function(){
      it('should handle rejection', function(){
         $scope.meta = $scope.get_meta();
         $scope.meta.rejection = {patient_choice: true};
         $scope.meta.rejection.date = "01/02/2015";
         var expectOpatOutcome = {
           patient_choice: true,
           date: "01/02/2015",
           episode_id: 33
         };
         var expectedTagging = {
            id:33, opat_referrals: false, "opat": false
         };
         var expectedEpisode = {
            id: 33, end: "01/02/2015", start: null
         }
         $httpBackend.expectPOST('/api/v0.1/opat_outcome/', expectOpatOutcome).respond({});
         $httpBackend.expectPUT('/api/v0.1/tagging/33/', expectedTagging).respond({});
         $httpBackend.expectPOST('/api/v0.1/opat_meta/', {episode_id: 33}).respond({});
         $httpBackend.expectPUT('/api/v0.1/episode/33/', expectedEpisode).respond({
           demographics: [{id: 1231, patient_id: 12312}]
         });
         $scope.reject();
         $httpBackend.flush();
      });
    });

    describe('accept', function(){
      it('should accept its fate', function(){
        var expectedTagging = {
           id:33, opat_referrals:false, opat_current:true, opat: true
        };
        var today = moment().format("DD/MM/YYYY");
        var expectedLocation = {id: 1, opat_acceptance: today};
        var expectedEpisode = {
           id: 33, start: expectedLocation.opat_acceptance, end: null
        }
        var todaty = moment().format("DD/MM/YYYY");
        $httpBackend.expectPUT('/api/v0.1/tagging/33/', expectedTagging).respond({});
        $httpBackend.expectPUT('/api/v0.1/location/1/', expectedLocation).respond({});
        $httpBackend.expectPUT('/api/v0.1/episode/33/', expectedEpisode).respond({
          demographics: [{id: 1231, patient_id: 12312}]
        });
        $scope.accept();
        $httpBackend.flush();
      });
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
                end: moment().format('DD/MM/YYYY'),
                id: 33,
                start: null
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

        it('Should close the modal', function () {
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
