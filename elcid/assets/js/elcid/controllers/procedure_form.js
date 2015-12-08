angular.module('opal.controllers').controller(
  'ProcedureFormCtrl', function($scope, Options) {
    "use strict";
    var vm = this;
    vm.editing = {procedure_type: undefined};
    vm.procedureTypes = ["medical", "surgical"];
    vm.procedures = [];
    vm.selectedProcedure = "";

    if(!$scope.editing.procedure){
      $scope.editing.procedure = {};
    }

    Options.then(function(options){
      vm.procedures = _.union(options.medicalprocedure, options.surgicalprocedure);

      $scope.$watch(angular.bind(vm, function () {
          return this.selectedProcedure;
      }), function(procedureType){
          if(_.contains(options.medicalprocedure, vm.selectedProcedure)){
              $scope.editing.procedure.medical_procedure = vm.selectedProcedure;
              $scope.editing.procedure.surgical_procedure = undefined;
          }
          else if(_.contains(options.surgical_procedure, vm.selectedProcedure)){
              $scope.editing.procedure.surgical_procedure = vm.selectedProcedure;
              $scope.editing.procedure.medical_procedure = undefined;
          }
      });
    });
});
