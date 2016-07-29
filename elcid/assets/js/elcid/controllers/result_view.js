angular.module('opal.controllers').controller('ResultView', function(){
      "use strict";
      var vm = this;
      this.filterValue = "";
      this.filter = function(item){
          if(!vm.filterValue){
            return true;
          }

          return item.profile_description.toLowerCase().indexOf(vm.filterValue.toLowerCase()) > -1
      }
});
