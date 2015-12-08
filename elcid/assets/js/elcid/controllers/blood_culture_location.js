controllers.controller('BloodCultureLocationCtrl',
  function(Options) {
      "use strict";
      var vm = this;
      vm.tagging_display_list = [];
      vm.display_tag_to_name = {};
      vm.selectedTags = [];

      Options.then(function(options){
        vm.tagging_display_list = _.values(options.tag_display);
        vm.display_tag_to_name = _.invert(options.tag_display);
      });

      vm.toSave = function(currentScope){
        currentScope.editing.tagging = _.map(vm.selectedTags, function(t){
            return vm.display_tag_to_name[t];
        });
      };

      vm.valid = function(){
        return true;
      };
});
