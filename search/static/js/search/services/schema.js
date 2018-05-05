angular.module('opal.services').factory('Schema', function() {
    "use strict";
    var Schema = function(rules){
      this.rules = angular.copy(rules);
      _.each(this.rules, function(c){
        _.each(c.fields, function(f){
          if(f.rule){
            throw 'the subrecord field has been declared on a namespace we need'
          }
          f.rule = c;
        });
      });
    };

    Schema.prototype = {
      findRule: function(ruleName){
        if(!ruleName){
          return;
        }
        return _.findWhere(this.rules, {name: ruleName});
      },
      findField: function(ruleName, fieldName){
        /*
        * returns the field object from the schema when given column.name and field.name
        */
        var rule = this.findRule(ruleName);
        if(!rule){return;}
        return _.findWhere(
            rule.fields, {name: fieldName}
        );
      },
      getChoices: function(rule, field, referencedata){
        var modelField = this.findField(rule, field);

        if(modelField.lookup_list && modelField.lookup_list.length){
          return referencedata.get(modelField.lookup_list);
        }

        if(modelField.enum){
          return modelField.enum;
        }
      },
      getFields: function(){
        // returns all fields
        var result = []
        _.each(this.rules, function(c){
          result = result.concat(c.fields);
        });
      }
    }

    return Schema
});
