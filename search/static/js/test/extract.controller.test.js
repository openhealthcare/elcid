describe('ExtractCtrl', function(){
    "use strict";

    var $scope, $httpBackend, schema, $window, $timeout, $modal, Item;
    var PatientSummary, $controller, ExtractSchema, controller, $rootScope;
    var extractQuerySchema, Schema;

    var referencedata = {
      dogs: ['Poodle', 'Dalmation'],
      hats: ['Bowler', 'Top', 'Sun'],
      toLookuplists: function(){
        return {
          dogs_list: ['Poodle', 'Dalmation'],
          hats_list: ['Bowler', 'Top', 'Sun']
        };
      }
    }

    var columnsData = [
        {
            "single":false,
            "name":"demographics",
            "display_name":"Demographics",
            "readOnly": true    ,
            "fields":[
                {
                    "display_name":"Name",
                    "lookup_list":null,
                    "name":"name",
                    "type":"string"
                },
                {
                    "display_name": "Deceased",
                    "lookup_list": null,
                    "name": "dead",
                    "type": "boolean"
                },
                {
                    "default": null,
                    "description": null,
                    "enum": null,
                    "lookup_list": "gender",
                    "model": "Demographics",
                    "name": "sex",
                    "display_name": "Sex",
                    "type": "string"
                },
                {
                    "display_name": "Age",
                    "lookup_list": null,
                    "name": "age",
                    "type": "integer"
                },
                {
                    "display_name": "Date of Birth",
                    "lookup_list": null,
                    "name": "date_of_birth",
                    "type": "date"
                },
                {
                    "display_name": "Last Appointment",
                    "lookup_list": null,
                    "name": "last_appointment",
                    "type": "date_time"
                },
            ]
        },
        {
            "single": false,
            "name": "symptoms",
            "display_name": "Symptoms",
            "readOnly": false,
            "fields": [
                {
                    "display_name": "Symptoms",
                    "lookup_list": "symptoms",
                    "name": "symptoms",
                    "type": "many_to_many"
                },
                {
                    "display_name":"Created",
                    "lookup_list":null,
                    "name":"created",
                    "type":"date_time"
                }
            ]
        }
    ];


    beforeEach(function(){
        module('opal.controllers');
        inject(function($injector){

            $rootScope  = $injector.get('$rootScope');
            $scope      = $rootScope.$new();
            $httpBackend = $injector.get('$httpBackend');
            $window      = $injector.get('$window');
            $modal       = $injector.get('$modal');
            $timeout     = $injector.get('$timeout');
            PatientSummary = $injector.get('PatientSummary');


            $controller  = $injector.get('$controller');
            ExtractSchema = $injector.get('ExtractSchema');
        });

        var extractQuerySchema = new ExtractSchema(angular.copy(columnsData));
        var extractSliceSchema = new ExtractSchema(angular.copy(columnsData));

        var controller = $controller('ExtractCtrl',  {
            $scope : $scope,
            $modal: $modal,
            $window: $window,
            extractQuerySchema : extractQuerySchema,
            extractSliceSchema : extractSliceSchema,
            PatientSummary: PatientSummary,
            referencedata: referencedata,
            extractQuery: null
        });

        $scope.$apply();
    });

    describe('set up', function(){
      it('should default the page state to query', function(){
        expect($scope.state).toBe('query');
      });

      it('should put reference data on the scope', function(){
        expect($scope.referencedata).toBe(referencedata);
      });

      it('should set up the schema on the scope', function(){
        expect(!!$scope.extractQuerySchema.rules).toBe(true);
      });

      it('should set the selected info', function(){
        expect($scope.sliceRule.name).toBe('demographics');
      });

      it('should set the extractSliceInfo', function(){
        expect($scope.extractSliceInfo.name).toBe('name');
      });
    });

    describe('refresh', function(){
        it('should reset the searched critera', function(){
            $scope.searched = true;
            $scope.refresh();
            expect($scope.searched).toBe(false);
        });

        it('should reset async waiting', function(){
          $scope.async_waiting = true;
          $scope.refresh();
          expect($scope.async_waiting).toBe(false);
        });

        it('should reset async ready', function(){
          $scope.async_ready = true;
          $scope.refresh();
          expect($scope.async_ready).toBe(false);
        });

        it('should clean the results', function(){
          $scope.results = [{something: "interesting"}];
          $scope.refresh();
          expect($scope.results).toEqual([]);
        });
    });

    describe('getQueryParams', function(){
      it('should get the critera and the page number', function(){
          var criteria = [{
              combine    : "and",
              rule       : "symptoms",
              field      : "symptoms",
              query_type : "contains",
              query      : "cough",
              lookup_list: []
          }];
          $scope.extractQuery.criteria = criteria;
          var expected = angular.copy(criteria);
          expected[0]["page_number"] = 1;
          expect($scope.getQueryParams(1)).toEqual(expected);
      });

      it('should remove the hash key', function(){
          var expected = [{
              combine    : "and",
              rule       : "symptoms",
              field      : "symptoms",
              query_type : "contains",
              query      : "cough",
              lookup_list: [],
          }];

          var criteria = angular.copy(expected);
          criteria["%%hashKey"] = 123;
          $scope.extractQuery.criteria = criteria;
          var expected = angular.copy(criteria);
          expected[0]["page_number"] = 1;
          expect($scope.getQueryParams(1)).toEqual(expected);
      });

      it('should copy the criteria', function(){
        var criteria = [{
            combine     : "and",
            rule        : "symptoms",
            field       : "symptoms",
            query_type  : "contains",
            query       : "cough",
            lookup_list: []
        }];
        $scope.extractQuery.criteria = criteria;
        criteria[0].page_number = 1;
        expect($scope.getQueryParams(1)).toEqual(criteria);
        expect($scope.getQueryParams(1)).not.toBe(criteria);
      });
    });

    describe('Search', function(){
        it('should ask the server for results', function(){

            $httpBackend.expectPOST("/search/extract/").respond({
                page_number: 1,
                total_pages: 1,
                total_count: 0,
                object_list: [
                    {categories: []}
                ]
            });
            $httpBackend.expectGET('/api/v0.1/userprofile/').respond({roles: {default: []}});
            $scope.extractQuery.criteria[0] = {
                combine    : "and",
                rule       : "symptoms",
                field      : "symptoms",
                query_type : "contains",
                query      : "cough",
                lookup_list: []
            }
            $scope.search();
            if(!$rootScope.$$phase) {
                $rootScope.$apply();
            }
            $httpBackend.flush();
            $httpBackend.verifyNoOutstandingExpectation();
            $httpBackend.verifyNoOutstandingRequest();
            expect($scope.searched).toBe(true);
        });

        it('should not replace the search results if they have subsequently been updated the criteria', function(){
            $httpBackend.expectPOST("/search/extract/").respond({
                page_number: 1,
                total_pages: 1,
                total_count: 0,
                object_list: [
                    {
                      categories: [],
                      first_name: "Wilma"
                    }
                ]
            });

            $scope.extractQuery.criteria[0] = {
                combine    : "and",
                rule       : "symptoms",
                field      : "symptoms",
                query_type : "contains",
                query      : "cough",
                lookup_list: []
            };

            $scope.search();

            $scope.extractQuery.criteria[0] = {
                combine    : "and",
                rule       : "diagnosis",
                field      : "condition",
                query_type : "contains",
                query      : "cough",
                lookup_list: []
            };

            $httpBackend.flush();
            $httpBackend.verifyNoOutstandingExpectation();
            $httpBackend.verifyNoOutstandingRequest();
            // the results should not be updated because the query has changed
            expect($scope.results.length).toBe(0);
        });

        it('should handle errors', function(){
            spyOn($window, 'alert');
            $httpBackend.expectPOST('/search/extract/').respond(500, {});
            $scope.extractQuery.criteria[0] = {
                combine    : "and",
                rule       : "symptoms",
                field      : "symptoms",
                query_type : "contains",
                query      : "cough",
                lookup_list: []
            }
            $scope.search();
            $httpBackend.flush();

            expect($window.alert).toHaveBeenCalled();
        });

        it('should handle not send a search if there are no criteria', function(){
            $scope.search();
            expect($scope.searched).toBe(true);
            $httpBackend.verifyNoOutstandingExpectation();
        });
    });

    describe('async_extract', function() {

        it('should open a new window if async_ready', function() {
            $scope.async_ready = true;
            $scope.extract_id = '23';
            spyOn($window, 'open');
            $scope.async_extract();

            expect($window.open).toHaveBeenCalledWith('/search/extract/download/23', '_blank');
        });

        it('should return null if async_waiting', function() {
            $scope.async_waiting = true;
            expect($scope.async_extract()).toBe(null);
        });

        it('should post to the url', function() {
            $httpBackend.expectPOST('/search/extract/download').respond({extract_id: '23'});
            $httpBackend.expectGET('/search/extract/status/23').respond({state: 'SUCCESS'})
            $scope.async_extract();
            $timeout.flush()
            $rootScope.$apply();
            $httpBackend.flush();

            expect($scope.extract_id).toBe('23');
            $rootScope.$apply();

            expect($scope.async_ready).toBe(true);
        });

        it('should re-ping', function() {
            $httpBackend.expectPOST('/search/extract/download').respond({});
            $scope.async_extract();
            $timeout.flush()
            $rootScope.$apply();
            $httpBackend.flush();
            $timeout.flush()
        });

        it('should re-ping if we are pending', function(){
            $httpBackend.expectPOST('/search/extract/download').respond({extract_id: '349'});
            var status_counter = 0;
            var status_responder = function(){
                if(status_counter == 0){
                    status_counter ++;
                    return [200, {state: 'PENDING'}]
                }
                return [200, {state: 'SUCCESS'}];
            }
            $httpBackend.when('GET', '/search/extract/status/349').respond(status_responder)
            $scope.async_extract();
            $timeout.flush()
            $rootScope.$apply();
            $httpBackend.flush();

            $timeout.flush()
            $rootScope.$apply();
            $httpBackend.flush();
            expect($scope.async_ready).toBe(true);
        });

        it('should alert if we fail', function() {
            $httpBackend.expectPOST('/search/extract/download').respond({extract_id: '23'});
            $httpBackend.expectGET('/search/extract/status/23').respond({state: 'FAILURE'})
            spyOn($window, 'alert');
            $scope.async_extract();
            $timeout.flush()
            $rootScope.$apply();
            $httpBackend.flush();

            expect($scope.extract_id).toBe('23');
            $rootScope.$apply();

            expect($scope.async_ready).toBe(false);
            expect($window.alert).toHaveBeenCalledWith('FAILURE');
        });

        it('should query with a data slice', function(){
          $scope.extractQuery.criteria = [{
            "rule": "demographics",
            "field": "first_name",
            "query_type":"Contains",
            "query":"a",
            "combine":"and"
          }];
          spyOn($scope.extractQuery, "getDataSlicesToSend").and.returnValue([{
            "demographics": ["first_name", "surname"]
          }]);

          var expected = {
            criteria: JSON.stringify([{
              "rule": "demographics",
              "field": "first_name",
              "query_type":"Contains",
              "query":"a",
              "combine":"and"
            }]),
            data_slice: JSON.stringify([{
              "demographics": ["first_name", "surname"]
            }])
          };

          $httpBackend.expectPOST('/search/extract/download', expected).respond({extract_id: '23'});
          $httpBackend.expectGET('/search/extract/status/23').respond({state: 'SUCCESS'})

          $scope.async_extract(true);
          $timeout.flush()
          $rootScope.$apply();
          $httpBackend.flush();

          expect($scope.extract_id).toBe('23');
          $rootScope.$apply();

          expect($scope.async_ready).toBe(true);
        });
    });

    describe('selectSliceRule', function(){
      it('should select the slice subrecord', function(){
        $scope.selectSliceRule("something");
        expect($scope.sliceRule).toBe("something");
      });
    });

    describe('setExtractSliceInfo', function(){
      it('should set the field info', function(){
        $scope.setExtractSliceInfo("something");
        expect($scope.extractSliceInfo).toBe("something");
      });
    });
});
