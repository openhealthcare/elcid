describe('ExtractQuery', function(){
  "use strict";

  var ExtractQuery, someQuery, criteria;

  var _criteria = [{
    combine: "and",
    field: "drug",
    query_type: "Contains",
    rule: "Allergies",
    value: "a"
  }];
  var field1 = {
    rule: "Allergies",
    name: "drug",
    default: null,
    desciption: null,
    display_name: "Drug"
  };

  var field2 = {
    rule: "Allergies",
    name: "provisional",
    default: null,
    desciption: null,
    display_name: "Provisional"
  };

  var rule = {
    display_name: "Allergies",
    name: "allergies",
    fields: [field1, field2]
  }
  field1.rule = rule;
  field2.rule = rule;

  var requiredFields = [field1];

  beforeEach(function(){
    module('opal.services');
    criteria = angular.copy(_criteria);
    inject(function($injector){
      ExtractQuery  = $injector.get('ExtractQuery');
      someQuery = angular.copy({
        criteria: criteria,
        slices: [field1, field2]
      });
    });
  });


  describe('setUp', function(){
    describe("load in existing query", function(){
      it('should load in an existing query', function(){
        var extractQuery = new ExtractQuery(requiredFields, someQuery);
        expect(extractQuery.criteria).toBe(someQuery.criteria);
        expect(extractQuery.slices).toBe(someQuery.slices)
      });

      it('should set the criteria to all for an existing query', function(){
        var extractQuery = new ExtractQuery(requiredFields, someQuery);
        expect(extractQuery.anyOrAll).toBe("all");
      });

      it('should set the criteria to any for an existing query', function(){
        var ourQuery = angular.copy(someQuery);
        ourQuery.criteria[0].combine = "or";
        var extractQuery = new ExtractQuery(requiredFields, ourQuery);
        expect(extractQuery.anyOrAll).toBe("any");
      });
    });

    describe("sets up the a basic query", function(){
      it("should set the required fields", function(){
        var extractQuery = new ExtractQuery(requiredFields);
        expect(extractQuery.requiredExtractFields).toEqual(requiredFields);
        expect(extractQuery.slices).toEqual(requiredFields);
        expect(extractQuery.criteria).toEqual([{}]);
        expect(extractQuery.anyOrAll).toBe("all");
      });
    });
  });

  describe("resetExtractSlice", function(){
    it("reset all slices to the required fields", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.slices = [field1, field2];
      extractQuery.resetExtractSlice();
      expect(extractQuery.slices).toEqual(requiredFields);
    });
  });

  describe("addSlice", function(){
    it("should add the slice if the slice is currently not added", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.addSlice(field2);
      expect(extractQuery.slices).toEqual([field1, field2]);
    });

    it("should not add the slice if the slice is already added", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.addSlice(field1);
      expect(extractQuery.slices).toEqual([field1]);
    });
  });

  describe("isRuleAdded", function(){
    it("should return true if the rule is added", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.addSlice(field2);
      expect(extractQuery.isRuleAdded(rule)).toBe(true);
    });

    it("should return false if the subrecord is not added", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      expect(extractQuery.isRuleAdded(rule)).toBe(false);
    });
  });

  describe("isSliceAdded", function(){
    it("should return true if a field is added is added", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      expect(extractQuery.isSliceAdded(field1)).toBe(true);
    });

    it("should return false if a subrecord is not added", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      expect(extractQuery.isSliceAdded(field2)).toBe(false);
    });
  });

  describe("addRuleSlices", function(){
    it("should add all slices for a rule", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      expect(extractQuery.isSliceAdded(field2)).toBe(false);
      extractQuery.addRuleSlices(rule);
      expect(extractQuery.isSliceAdded(field2)).toBe(true);
    });
  });

  describe("removeRuleSlices", function(){
    it("should remove remove all slices for a subrecord", function(){
      // an extract query with no required fields
      var extractQuery = new ExtractQuery([]);
      extractQuery.addRuleSlices(rule);
      extractQuery.removeRuleSlices(rule);
      expect(extractQuery.isSliceAdded(field1)).toBe(false);
      expect(extractQuery.isSliceAdded(field2)).toBe(false);
    });

    it("should not remove required fields", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.addRuleSlices(rule);
      extractQuery.removeRuleSlices(rule);
      expect(extractQuery.isSliceAdded(field1)).toBe(true);
      expect(extractQuery.isSliceAdded(field2)).toBe(false);
    });
  });

  describe("removeSlice", function(){
    it("should find and remove a slice if its not required", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.addSlice(field2);
      extractQuery.removeSlice(field2);
      expect(extractQuery.isSliceAdded(field2)).toBe(false);
    });

    it("should not remove the slice if it is required", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.removeSlice(field1);
      expect(extractQuery.isSliceAdded(field1)).toBe(true);
    });
  });

  describe("sliceIsRequired", function(){
    it("should return true if a slice is required", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      expect(extractQuery.sliceIsRequired(field1)).toBe(true);
    });

    it("should return false if a slice is not required", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      expect(extractQuery.sliceIsRequired(field2)).toBe(false);
    });
  });

  describe("getDataSlicesToSend", function(){
    it("should return a rule to field name arrary", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.addSlice(field2);
      expect(extractQuery.getDataSlicesToSend()).toEqual(
        {allergies: [ 'drug', 'provisional' ]}
      );
    });
  });

  describe("getCriteriaToSend", function(){
    it("should create the search criteria to send to the server", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.criteria = criteria;
      expect(extractQuery.getCriteriaToSend()).toEqual([
        {
          combine: 'and',
          field: 'drug',
          query_type: 'Contains',
          rule: 'Allergies',
          value: 'a'
        }
      ]);
    });
  });

  describe("completeCriteria", function(){
    it('should return the complete criteria', function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.criteria = criteria;
      var extractQuerySchema = jasmine.createSpyObj(["findField"]);
      extractQuerySchema.findField.and.returnValue({
        query_args: ["value", "query_type"]
      });
      expect(extractQuery.completeCriteria(extractQuerySchema)).toEqual(criteria);
    });

    it("should return false if the criteria is not complete", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.criteria = criteria;
      var extractQuerySchema = jasmine.createSpyObj(["findField"]);
      extractQuerySchema.findField.and.returnValue({
        query_args: ["value", "query_type", "something_else"]
      });
      expect(extractQuery.completeCriteria(extractQuerySchema)).toEqual([]);
    });

    it("should ignore fields we can't find", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.criteria = criteria;
      var extractQuerySchema = jasmine.createSpyObj(["findField"]);
      extractQuerySchema.findField.and.returnValue(null);
      expect(extractQuery.completeCriteria(extractQuerySchema)).toEqual([]);
    });
  });

  describe("addFilter", function(){
    it("should add a filter", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.criteria = criteria;
      extractQuery.addFilter();
      expect(extractQuery.criteria[0]).toEqual(criteria[0]);
      expect(extractQuery.criteria.length).toBe(2);
      expect(extractQuery.criteria[1]).toEqual({});
    });
  });

  describe("removeFilter", function(){
    it("should remove replace the criteria with an empty obj if its the last one", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.criteria = criteria;
      extractQuery.removeFilter(0);
      expect(extractQuery.criteria).toEqual([{}]);
    });

    it("should just remove the element of an array if it is not the last one", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.criteria = criteria;
      extractQuery.criteria.push({
        rule: "Demographics", field: "date_of_birth"
      });
      extractQuery.removeFilter(1);
      expect(extractQuery.criteria).toEqual(criteria);
    });
  });

  describe("resetFilter", function(){
    it("should reset the current query", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.criteria = angular.copy(criteria);
      extractQuery.resetFilter(0, ["rule"])
      expect(extractQuery.value).toBe(undefined);
      expect(extractQuery.query_type).toBe(undefined);
      expect(extractQuery.field).toBe(undefined);
    });
  });

  describe("removeCriteria", function(){
    it("should completely resync the criteria", function(){
      var extractQuery = new ExtractQuery(requiredFields);
      extractQuery.criteria = angular.copy(criteria);
      extractQuery.removeCriteria();
      expect(extractQuery.criteria).toEqual([{}]);
    });
  });
});
