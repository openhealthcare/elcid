describe('Schema', function(){
  "use strict";

  var Schema, schema;

  var exampleSchemaData = [
      {
          "single":false,
          "name":"demographics",
          "display_name":"Demographics",
          "readOnly": true    ,
          "fields":[
              {
                  "title":"Name",
                  "lookup_list":null,
                  "name":"name",
                  "type":"string"
              },
              {
                  "title": "Deceased",
                  "lookup_list": null,
                  "name": "dead",
                  "type": "boolean"
              },
              {
                  "title": "Date of Birth",
                  "lookup_list": null,
                  "name": "date_of_birth",
                  "type": "date"
              },
              {
                  "title": "Age",
                  "lookup_list": null,
                  "name": "age",
                  "type": "integer"
              },
              {
                  "title": "Last Appointment",
                  "lookup_list": null,
                  "name": "last_appointment",
                  "type": "date_time"
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
              title: "Test",
              type: "string"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "MicrobiologyTest",
              name: "date_ordered",
              title: "Date Ordered",
              type: "date"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "MicrobiologyTest",
              name: "details",
              title: "Details",
              type: "string"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "MicrobiologyTest",
              name: "microscopy",
              title: "Microscopy",
              type: "string"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "MicrobiologyTest",
              name: "organism",
              title: "Organism",
              type: "string"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "MicrobiologyTest",
              name: "sensitive_antibiotics",
              title: "Sensitive Antibiotics",
              type: "string"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "MicrobiologyTest",
              name: "resistant_antibiotics",
              title: "Resistant Antibiotics",
              type: "string"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "MicrobiologyTest",
              name: "igm",
              title: "IGM",
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
              title: "Test",
              type: "string"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "Investigation",
              name: "date_ordered",
              title: "Date Ordered",
              type: "date"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "Investigation",
              name: "details",
              title: "Details",
              type: "string"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "Investigation",
              name: "microscopy",
              title: "Microscopy",
              type: "string"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "Investigation",
              name: "organism",
              title: "Organism",
              type: "string"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "Investigation",
              name: "sensitive_antibiotics",
              title: "Sensitive Antibiotics",
              type: "string"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "Investigation",
              name: "resistant_antibiotics",
              title: "Resistant Antibiotics",
              type: "string"
            },
            {
              default: null,
              description: null,
              enum: null,
              lookup_list: null,
              model: "Investigation",
              name: "igm",
              title: "IGM",
              type: "string"
            },
          ],
      },
      {
          "single": false,
          "name": "symptoms",
          "display_name": "Symptoms",
          "readOnly": false,
          "fields": [
              {
                  "title": "Symptoms",
                  "lookup_list": "symptoms",
                  "name": "symptoms",
                  "type": "many_to_many"
              },
              {
                  "title":"Consistency Token",
                  "lookup_list":null,
                  "name":"consistency_token",
                  "type":"token"
              },
              {
                  "title":"Created",
                  "lookup_list":null,
                  "name":"created",
                  "type":"date_time"
              }
          ]
      }
  ];

  beforeEach(function(){
    module('opal.services');

    inject(function($injector) {
        Schema = $injector.get('Schema');
    })

    schema = new Schema(exampleSchemaData);
  });

  it('should return the find the field', function(){
    expect(!!schema.findField("demographics", "name")).toEqual(true);
  });

  it('should set up a reference on fields to the subrecord', function(){
      expect(schema.columns[0].fields[0].subrecord).toBe(schema.columns[0]);
  });

  it('should throw an error if the subrecord field has already been populated', function(){
    var flawedSchemaData = angular.copy(exampleSchemaData);
    flawedSchemaData[0].fields[0].subrecord = "bah";
    expect(function(){ new Schema(flawedSchemaData);}).toThrow();
  });

  describe('getChoices', function(){
    it('should get a lookup list and suffix it', function(){
      spyOn(schema, "findField").and.returnValue({
        lookup_list: "dogs"
      });
      var referencedata = jasmine.createSpyObj(["get"])
      referencedata.get.and.returnValue(['Poodle', 'Dalmation']);
      var result = schema.getChoices("some", "field", referencedata);
      expect(result).toEqual(['Poodle', 'Dalmation']);
      expect(referencedata.get).toHaveBeenCalledWith("dogs");
    });

    it('should get an enum', function(){
      spyOn(schema, "findField").and.returnValue({
        enum: [1, 2, 3]
      });
      var result = schema.getChoices("some", "field");
      expect(result).toEqual([1, 2, 3]);
    });
  });
});
