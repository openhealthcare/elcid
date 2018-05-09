angular.module('opal.services').factory('ExtractQuery', function(){
  "use strict";

  var ExtractQuery = function(extractQuerySchema, extractSliceSchema, queryParams){
    this.requiredExtractFields = [];
    this.slices = [];
    this.extractQuerySchema = extractQuerySchema;
    this.extractSliceSchema = extractSliceSchema;

    // whether the user would like an 'or' conjunction or and 'and'
    this.combinations = ["all", "any"];
    _.each(extractSliceSchema.getFields(), function(f){
      if(f.required){
        this.requiredExtractFields.push(f)
      }
    }, this);

    // the seatch query
    if(queryParams){
      this.criteria = queryParams.criteria;
      // this.slices = queryParams.slices;
      _.each(queryParams.data_slice, function(fields, ruleName){
        _.each(fields, function(field){
          var slice = this.extractSliceSchema.findField(ruleName, field);
          if(slice){
            this.slices.push(
              slice
            );
          }
        }, this);
      }, this);
      if(this.criteria[0].combine === 'and'){
        this.anyOrAll = "all";
      }
      else{
        this.anyOrAll = "any";
      }
    }
    else{
      // the rules in the download
      // shallow copies ftw
      this.slices = _.clone(this.requiredExtractFields);
      this.criteria = [{}];
      this.anyOrAll = this.combinations[0];
    }
  };

  ExtractQuery.prototype = {
    getRequiredFields: function(){

    },
    reset: function(){
      this.slices = _.clone(this.requiredExtractFields);
    },
    addSlice: function(someField){
      // add a field to the extract fields
      if(!this.isSliceAdded(someField)){
        this.slices.push(someField);
      }
    },
    isSubrecordAdded: function(someRule){
      return someRule.fields.length === _.filter(this.slices, function(field){
        return field.rule === someRule;
      }).length;
    },
    isSliceAdded: function(someField){
      return _.indexOf(this.slices, someField) !== -1
    },
    addSubrecordSlices: function(someRule){
      // adds all fields for a rule
      _.each(someRule.fields, this.addSlice, this);
    },
    removeSubrecordSlices: function(someRule){
      // adds all fields for a rule
      _.each(someRule.fields, this.removeSlice, this);
    },
    removeSlice: function(someField){
      // remove a field from the extract fields
      this.slices = _.filter(this.slices, function(slicedField){
        return someField !== slicedField || this.sliceIsRequired(slicedField);
      }, this);
    },
    sliceIsRequired: function(someField){
      return _.indexOf(this.requiredExtractFields, someField) !== -1;
    },
    getDataSlices: function(){
      var result = {}
      _.each(this.slices, function(field){
        if(!(field.rule.name in result)){
          result[field.rule.name] = [];
        }
        result[field.rule.name].push(
          field.name
        );
      });
      return result;
    },
    getCriteriaToSend: function(){
      // remove the angular hash key
      var result = [];
      _.each(this.criteria, function(query){
        var query_row = {};
        _.each(query, function(v, k){
            if(k !== "$$hashKey"){
              query_row[k] = v;
            }
        });
        result.push(query_row);
      });

      return result;
    },
    completeCriteria: function(){
      var combine;
      // queries can look at either all of the options, or any of them
      // ie 'and' conjunctions or 'or'
      if(this.anyOrAll === 'all'){
        combine = "and";
      }
      else{
        combine = 'or';
      }

      // remove incomplete criteria
      criteria = _.filter(this.criteria, function(c){
          var field = this.extractQuerySchema.findField(c.rule, c.field);
          if(!field){
            return false;
          }

          result = _.all(field.query_args, function(queryArg){
            return !!c[queryArg];
          });

          // If not, we ignore this clause
          return result;
      }, this);

      _.each(criteria, function(c){
        c.combine = combine;
      });

      return criteria
    },
    addFilter: function(){
        this.criteria.push({});
    },
    removeFilter: function(index){
        if(this.extractQueryInfo === this.criteria[index]){
          this.extractQueryInfo = undefined;
        }
        if(this.criteria.length == 1){
            this.removeCriteria();
        }
        else{
            this.criteria.splice(index, 1);
        }
    },
    resetFilter: function(queryRow, fieldsTypes){
      // when we change the rule, reset the rest of the query
      _.each(queryRow, function(v, k){
        if(!_.contains(fieldsTypes, k)){
          queryRow[k] = undefined;
        }
      });
    },
    removeCriteria: function(){
        this.criteria = [{}];
    }
  }

  return ExtractQuery;
});
