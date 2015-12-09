controllers.controller('BloodCultureLocationCtrl',
  function(Options, $controller) {
      "use strict";
      var parentCtrl = $controller("MultistageDefault");
      var vm = this;

      _.extend(vm, parentCtrl);
      vm.tagging_display_list = [];
      vm.display_tag_to_name = {};
      vm.selectedTags = [];

      Options.then(function(options){
        var direct_add = _.filter(options.tag_display, function(v, k){
            return _.contains(options.tag_direct_add, k);
        });
        vm.tagging_display_list = _.values(direct_add);
        vm.display_tag_to_name = _.invert(options.tag_display);
      });

      vm.toSave = function(currentScope){
        currentScope.editing.tagging = _.map(vm.selectedTags, function(t){
            return vm.display_tag_to_name[t];
        });
      };
});
