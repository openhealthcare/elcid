describe('DischargePatientService', function(){
  "use strict";
  var episode, dischargePatientService, tags, tagging, location, $rootScope;
  var DischargePatientService, editing, opalTestHelper;

  beforeEach(function(){
    module('opal.services', function($provide) {
        $provide.value('UserProfile', function(){ return profile; });
    });

    module('opal.test');

    inject(function($injector){
      $rootScope   = $injector.get('$rootScope');
      DischargePatientService = $injector.get('DischargePatientService');
      opalTestHelper = $injector.get('opalTestHelper');
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
          return this;
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
        return this;
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
      },
      location: [location]
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

    it("should set the end date appropriately if there's an end date that is a moment", function(){
    var episode = opalTestHelper.newEpisode($rootScope);
    var expectedDate = moment("2016-05-25");
    // validate assumptions
    expect(expectedDate.isSame(episode.end)).toBe(true);
    dischargePatientService = new DischargePatientService(episode, tags);
    var editing = dischargePatientService.getEditing(episode);
    expect(editing.end).toEqual(expectedDate.toDate());
  });

  it("should set the end date appropriately if end is not set", function(){
    var end = new Date();
    episode.location = [{category: "Inpatient"}];
    dischargePatientService.getEditing(episode, tags);
    var editing = dischargePatientService.getEditing(episode);
    expect(editing.end).toEqual(end);
  });

    it("should discharge the patient, if the patient location was follow up", function(){
      var editing = {category: 'Followup'};
      var resolved = false;
      spyOn(location, "save").and.callThrough();
      location.category = "Followup";
      dischargePatientService.discharge(episode, editing, tags).then(function(){
        resolved = true;
      });
      $rootScope.$apply();
      expect(location.save.calls.mostRecent().args[0].category).toBe(
        'Discharged'
      );
    });

    it("should not discharge the patient, if the patient location was not follow up", function(){
      var editing = {category: ''};
      var resolved = false;
      spyOn(location, "save").and.callThrough();
      location.category = "";
      dischargePatientService.discharge(episode, editing, tags).then(function(){
        resolved = true;
      });
      $rootScope.$apply();
      expect(location.save.calls.mostRecent().args[0].category).toBe(
        ''
      );
    });
  });
});
