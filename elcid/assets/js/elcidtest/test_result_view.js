describe('ResultViewTest', function() {
  "use strict";

  var controller;
  beforeEach(function(){
      var $controller;
      module('opal.controllers');

      inject(function($injector){
          $controller  = $injector.get('$controller');
      });

      controller = $controller('ResultView');
  });

  describe("it should filter items based on profile description", function(){
    it("should return false if the filter is not found", function(){
        controller.filterValue = "as"
        var item = {"profile_description": "bg"}
        expect(controller.filter(item)).toBe(false);
    });

    it("should return true with case insensitivty if the filter is found", function(){
      controller.filterValue = "aG"
      var item = {"profile_description": "Ag"}
      expect(controller.filter(item)).toBe(true);
    });

  });

});
