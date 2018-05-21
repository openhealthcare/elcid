describe('ExtractSchema', function(){
  "use strict";
  var ExtractSchema, schemaArgs, schema;
  var rule1, rule2, _field1, _field2, _field3;

  _field1 = {
    name: "drug",
    default: null,
    enum: null,
    lookup_list: "antimicrobial",
    desciption: null,
    display_name: "Drug",
    required: true
  };

  _field2 = {
    name: "provisional",
    default: null,
    desciption: null,
    display_name: "Provisional"
  };
  _field3 = {
    name: "duration",
    display_name: "Duration",
    default: null,
    desciption: null,
    icon: "fa fa-stethoscope",
    enum: [
      "3 days or less", "4-10 days", "11-21 days", "22 days to 3 months", "over 3 months"
    ]
  }


  beforeEach(function(){
    module('opal.services');

    rule1 = {
      display_name: "Allergies",
      name: "allergies",
      fields: [_field1, _field2]
    }

    rule2 = {
      display_name: "Presenting Complaint",
      name: "presenting_complaints",
      fields: [_field3]
    }

    inject(function($injector){
      ExtractSchema  = $injector.get('ExtractSchema');
      schema = new ExtractSchema(angular.copy([rule1, rule2]));
    });
  });

  describe("setUp", function(){
    it("should set up the rules", function(){
      var r = schema.rules[0];
      expect(r.fields[0].rule).toBe(r);
    });
  });

  describe("findRule", function(){
    it("should return null if no rule is passed in", function(){
      expect(schema.findRule("blah")).toBe(undefined);
    });

    it("should return the rule if it is found", function(){
      expect(schema.findRule("allergies")).toEqual(schema.rules[0]);
    });
  });

  describe("findField", function(){
    it("should return the field if it can be found", function(){
      expect(schema.findField("allergies", "drug")).toEqual(
        schema.rules[0].fields[0]
      );
    });

    it("should return undefined if the field cannot be found", function(){
      expect(schema.findField("allergies", "asfsfd")).toBe(undefined);
      expect(schema.findField("asdfsfd", "drug")).toBe(undefined);
    });

    it("should return undefined if no rule is passed in", function(){
      expect(schema.findField()).toBe(undefined);
    });
  });

  describe("getChoices", function(){
    it("should return the lookup list if it exists", function(){
      var referenceData = {get: function(){return ["paracetomol"]}};
      expect(schema.getChoices("allergies", "drug", referenceData)).toEqual(
        ["paracetomol"]
      )
    });

    it("should return the enum list it exists", function(){
      expect(schema.getChoices("presenting_complaints", "duration", null)).toEqual(
        _field3.enum
      )
    });

    it("should return undefined if there is no lookup list or enum", function(){
      expect(
        schema.getChoices("allergies", "provisional"),
        null
      )
    });
  });

  describe("getFields", function(){
    it("should return all of the fields as a list", function(){
        var fields = schema.getFields();
        _.each(fields, function(field){
          delete field.rule;
          return field;
        });
        expect(fields).toEqual([_field1, _field2, _field3]);
    });
  });

  describe("getRequiredFields", function(){
    it("should return all fields that are required", function(){
      var requiredFields = schema.getRequiredFields();
      _.each(requiredFields, function(field){
        delete field.rule;
        return field;
      });
      expect(requiredFields).toEqual([_field1]);
    });
  });
});
