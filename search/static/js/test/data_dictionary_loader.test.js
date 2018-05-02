describe('extractSliceSchemaLoader', function(){
    "use strict"

    var $httpBackend, $rootScope, extractSliceSchemaLoader;
    var mock, opalTestHelper;
    var dictionarySchema = {
        'demographics': {
            name: "demographics",
            fields: [
                {name: 'first_name', type: 'string'},
                {name: 'surname', type: 'string'},
                {name: 'date_of_birth', type: 'date'},
            ]
      }
    };

    beforeEach(function(){
        mock = { alert: jasmine.createSpy() };
        module('opal.services', function($provide){
            $provide.value('$window', mock);
        });
        module('opal.test');
        var mockSchema = function(x){ return x; };

        inject(function($injector){
            extractSliceSchemaLoader   = $injector.get('extractSliceSchemaLoader');
            $httpBackend   = $injector.get('$httpBackend');
            $rootScope     = $injector.get('$rootScope');
        });
    });

    it('should fetch the record data', function(){
        var result;
        $httpBackend.whenGET('/search/api/data_dictionary/').respond(dictionarySchema);
        extractSliceSchemaLoader.load().then(function(r){ result = r; });
        $rootScope.$apply()
        $httpBackend.flush();
        var expectedSubrecordNames = _.pluck(dictionarySchema, "name");
        var foundSubrecordNames = _.pluck(result.columns, "name");
        expect(expectedSubrecordNames).toEqual(foundSubrecordNames);
    });

    it('should alert if the HTTP request errors', function(){
        var result;
        $httpBackend.whenGET('/search/api/data_dictionary/').respond(500, 'NO');
        extractSliceSchemaLoader.load().then(function(r){ result = r; });
        $rootScope.$apply();
        $httpBackend.flush();
        expect(mock.alert).toHaveBeenCalledWith(
          'Data dictionary could not be loaded'
        );
    });
});
