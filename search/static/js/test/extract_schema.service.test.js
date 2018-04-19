describe('ExtractSchema', function(){
    "use strict";

    var ExtractSchema, schema;

    var exampleSchemaData = [
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
                }
            ]
        },
        {
            "name": "diagnosis",
            "single": false,
            "sort": 'date_of_diagnosis',
            "fields": [
                {"name": 'date_of_diagnosis', "type": 'date'},
                {"name": 'condition', "type": 'string'},
                {"name": 'provisional', "type": 'boolean'},
            ]
        },
        {
            "single": false,
            "name": "microbiology_test",
            "display_name": "Microbiology Test",
            "readOnly": false,
            "fields": [
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "MicrobiologyTest",
                name: "test",
                display_name: "Test",
                type: "string"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "MicrobiologyTest",
                name: "date_ordered",
                display_name: "Date Ordered",
                type: "date"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "MicrobiologyTest",
                name: "details",
                display_name: "Details",
                type: "string"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "MicrobiologyTest",
                name: "microscopy",
                display_name: "Microscopy",
                type: "string"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "MicrobiologyTest",
                name: "organism",
                display_name: "Organism",
                type: "string"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "MicrobiologyTest",
                name: "sensitive_antibiotics",
                display_name: "Sensitive Antibiotics",
                type: "string"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "MicrobiologyTest",
                name: "resistant_antibiotics",
                display_name: "Resistant Antibiotics",
                type: "string"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "MicrobiologyTest",
                name: "igm",
                display_name: "IGM",
                type: "string"
              },
            ],
        },
        {
            "single": false,
            "name": "investigation",
            "display_name": "Investigation",
            "readOnly": false,
            "fields": [
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "Investigation",
                name: "test",
                display_name: "Test",
                type: "string"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "Investigation",
                name: "date_ordered",
                display_name: "Date Ordered",
                type: "date"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "Investigation",
                name: "details",
                display_name: "Details",
                type: "string"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "Investigation",
                name: "microscopy",
                display_name: "Microscopy",
                type: "string"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "Investigation",
                name: "organism",
                display_name: "Organism",
                type: "string"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "Investigation",
                name: "sensitive_antibiotics",
                display_name: "Sensitive Antibiotics",
                type: "string"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "Investigation",
                name: "resistant_antibiotics",
                display_name: "Resistant Antibiotics",
                type: "string"
              },
              {
                default: null,
                description: null,
                enum: null,
                lookup_list: null,
                model: "Investigation",
                name: "igm",
                display_name: "IGM",
                type: "string"
              },
            ],
        }
    ];

    beforeEach(function(){
        module('opal.services');

        inject(function($injector) {
            ExtractSchema = $injector.get('ExtractSchema');
        })

        schema = new ExtractSchema(exampleSchemaData);
    });

    it('should keep a publically accessible version of columns', function(){
        var result = angular.copy(schema.columns);
        _.each(result, function(subrecord){
          _.each(subrecord.fields, function(field){
            delete field.subrecord;
          });
        });
        var expectedColumnNames = _.map(exampleSchemaData, function(c){ return c.name })
        var foundColumnNames = _.map(result, function(r){ return r.name });
        expect(foundColumnNames).toEqual(expectedColumnNames);
    });

    it('should restrict the fields to searchable fields for micro test', function(){
        var microTest = schema.findColumn('microbiology_test');
        var found = _.map(microTest.fields, function(mtf){
          return mtf.display_name;
        });
        var expected = [
          'Test',
          'Date Ordered',
          'Details',
          'Microscopy',
          'Organism',
          'Sensitive Antibiotics',
          'Resistant Antibiotics'
        ];

        expect(expected).toEqual(found);
    });

    it('should restrict the fields to searchable fields for investigations', function(){
        var microTest = schema.findColumn('microbiology_test');
        var found = _.map(microTest.fields, function(mtf){
          return mtf.display_name;
        });
        var expected = [
          'Test',
          'Date Ordered',
          'Details',
          'Microscopy',
          'Organism',
          'Sensitive Antibiotics',
          'Resistant Antibiotics'
        ];

        expect(expected).toEqual(found);
    });
});
