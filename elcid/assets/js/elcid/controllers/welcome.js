angular.module('opal.controllers').controller('WelcomeCtrl', function($location, options){
  "use strict";

  var vm = this;
  vm.editing = {team: ''};
  vm.path_base = '/list/';

  var visible_in_list = options.tag_visible_in_list;

  var display_to_tag_list = _.invert(options.tag_display);

  vm.tagList = _.map(visible_in_list, function(vl){
    return options.tag_display[vl];
  });

  vm.toLink = function(displayName){
      return display_to_tag_list[displayName]

  }

  vm.jumpToTag = function(){
      var tag = display_to_tag_list[vm.editing.team];
      if(_.contains(_.keys(options.tag_hierarchy), tag)){
          $location.path(vm.path_base + tag);
      }else{
          for(var prop in options.tag_hierarchy){
              if(options.tag_hierarchy.hasOwnProperty(prop)){
                  if(_.contains(_.values(options.tag_hierarchy[prop]), tag)){
                      $location.path(vm.path_base + prop + '/' + tag);
                  }
              }
          }
      }
  };
});
