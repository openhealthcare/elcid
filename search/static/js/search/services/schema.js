angular.module('opal.services').factory('Schema', function() {
    "use strict";
    var Schema = function(columns){
      this.columns = angular.copy(columns);
      _.each(this.columns, function(c){
        _.each(c.fields, function(f){
          if(f.subrecord){
            throw 'the subrecord field has been declared on a namespace we need'
          }
          f.subrecord = c;
        });
      });
    };

    Schema.prototype = {
      findColumn: function(columnName){
        if(!columnName){
          return;
        }
        return _.findWhere(this.columns, {name: columnName});
      },
      findField: function(columnName, fieldName){
        /*
        * returns the field object from the schema when given column.name and field.name
        */
        var column = this.findColumn(columnName);
        if(!column){return;}
        return _.findWhere(
            column.fields, {name: fieldName}
        );
      },
      getChoices: function(column, field, referencedata){
        var modelField = this.findField(column, field);

        if(modelField.lookup_list && modelField.lookup_list.length){
          return referencedata.get(modelField.lookup_list);
        }

        if(modelField.enum){
          return modelField.enum;
        }
      }
    }

    return Schema
});
