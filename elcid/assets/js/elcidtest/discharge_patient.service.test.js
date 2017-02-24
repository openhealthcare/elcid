describe('DischargePatientService', function(){
  var episode, dischargePatientService, tags, tagging, location, $rootScope;

  beforeEach(function(){
    module('opal.services', function($provide) {
        $provide.value('UserProfile', function(){ return profile; });
    });

    inject(function($injector){
      $rootScope   = $injector.get('$rootScope');
      DischargePatientService = $injector.get('DischargePatientService');
    });

    tagging = {
      makeCopy: function(){
          return {};
      },
      save: function(){
        return {
          then: function(fn){
            fn();
          }
        };
      }
    };

    location = {
      makeCopy: function(){
          return {};
      },
      save: function(){
        return {
          then: function(fn){
            fn();
          }
        };
      }
    };

    episode = {
      makeCopy: function(){
        return {};
      },
      save: function(){
        return {
          then: function(fn){
            fn();
          }
        };
      },
      getItem: function(column){
        if(column === "location"){
          return location;
        }
        return tagging;
      }
    };

    tags = {
      tag: "infectious_diseases",
      subtag: "id_liason"
    };

    dischargePatientService = new DischargePatientService();
  });

  describe('discharge', function(){

    it("should set tags to false, if category isn't Followup", function(){
      var editing = {category: 'Discharged'};
      var resolved = false;
      spyOn(tagging, "save").and.callThrough();
      dischargePatientService.discharge(episode, editing, tags).then(function(){
        resolved = true;
      });
      $rootScope.$apply();
      expect(resolved).toBe(true);
      expect(tagging.save).toHaveBeenCalledWith({id_liason: false});
    });

    it("should not update tags, if category is Followup", function(){
      var editing = {category: 'Followup'};
      var resolved = false;
      spyOn(tagging, "save").and.callThrough();
      dischargePatientService.discharge(episode, editing, tags).then(function(){
        resolved = true;
      });
      $rootScope.$apply();
      expect(resolved).toBe(true);
      expect(tagging.save).toHaveBeenCalledWith({});
    });
  });
});
