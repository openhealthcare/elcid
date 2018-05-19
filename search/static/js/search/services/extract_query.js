angular.module('opal.services').factory('ExtractQuery', function(){
  "use strict";

  var ExtractQuery = function(requiredFields, queryParams){
    this.slices = [];
    this.requiredExtractFields = requiredFields;

    // whether the user would like an 'or' conjunction or and 'and'
    this.combinations = ["all", "any"];

    // the seatch query
    if(queryParams){
      this.criteria = queryParams.criteria;
      this.slices = queryParams.slices;
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
    resetExtractSlice: function(){
      this.slices = _.clone(this.requiredExtractFields);
    },
    addSlice: function(someField){
      // add a field to the extract fields
      if(!this.isSliceAdded(someField)){
        this.slices.push(someField);
      }
    },
    isRuleAdded: function(someRule){
      /* Have all the fields for a certain rule been added?
      */
      return someRule.fields.length === _.filter(this.slices, function(field){
        return field.rule === someRule;
      }).length;
    },
    isSliceAdded: function(someField){
      return _.indexOf(this.slices, someField) !== -1
    },
    isQuerySelected: function(someQuery){
      // takes in a part of the query and returns whether it is selected
      return _.any(this.criteria, function(x){
        return x.rule === someQuery.rule.name && x.field === someQuery.name
      });
    },
    addRuleSlices: function(someRule){
      // adds all fields for a rule
      _.each(someRule.fields, this.addSlice, this);
    },
    removeRuleSlices: function(someRule){
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
    getDataSlicesToSend: function(){
      /*
        it should return an array to send back to the server of the data
        slicers
        {ruleName: [fieldName1, fieldName2]}
      */
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
      /*
        it should return all the compiled search query to send to the
        server
      */
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
    completeCriteria: function(extractQuerySchema){
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
      var criteria = _.filter(this.criteria, function(c){
          var field = extractQuerySchema.findField(c.rule, c.field);
          if(!field){
            return false;
          }

          var result = _.all(field.query_args, function(queryArg){
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
