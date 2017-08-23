describe("LocationWardComparator", function(){
  "use strict";
  var LocationWardComparator, opalTestHelper, episodeData, $rootScope;
  var first, second;

  var locationData = [{
    hospital: "UCH",
    category: "Inepisode",
    ward: "T9",
    bed: 12
  }];

  beforeEach(function(){
    module('opal.services');
    module('opal.test');
    inject(function($injector){
      LocationWardComparator  = $injector.get('LocationWardComparator');
      opalTestHelper = $injector.get('opalTestHelper');
      $rootScope = $injector.get('$rootScope');
    });
    first = opalTestHelper.newEpisode($rootScope);
    second = opalTestHelper.newEpisode($rootScope);

    first.location = angular.copy(locationData);
    second.location = angular.copy(locationData);
  });

  it('it return an array of a four functions', function(){
    expect(_.isArray(LocationWardComparator)).toBe(true);
    expect(LocationWardComparator.length).toBe(4);
    _.each(LocationWardComparator, function(c){
      expect(_.isFunction(c)).toBe(true);
    });
  });

  it('it should compare by hospital', function(){
    first.location[0].hospital = "UCH";
    second.location[0].hospital = "RFH";
    expect(first.compare(second, LocationWardComparator)).toEqual(1);
    expect(second.compare(first, LocationWardComparator)).toEqual(-1);
  });

  it('should compare by category', function(){
    first.location[0].category = "Review";
    second.location[0].category = "Inepisode";
    expect(first.compare(second, LocationWardComparator)).toEqual(1);
    expect(second.compare(first, LocationWardComparator)).toEqual(-1);
  });

  it('should compare ward without number', function(){
    first.location[0].ward = "X-ray";
    second.location[0].ward = "A&E";
    expect(first.compare(second, LocationWardComparator)).toEqual(1);
    expect(second.compare(first, LocationWardComparator)).toEqual(-1);
  });

  it('should compare wards in the tower', function(){
    first.location[0].ward = "A&E";
    second.location[0].ward = "T3 something something";
    expect(first.compare(second, LocationWardComparator)).toEqual(1);
    expect(second.compare(first, LocationWardComparator)).toEqual(-1);
  });

  it('should compare wards in the tower with multiple digits', function(){
    first.location[0].ward = "T10";
    second.location[0].ward = "T3 something something";
    expect(first.compare(second, LocationWardComparator)).toEqual(1);
    expect(second.compare(first, LocationWardComparator)).toEqual(-1);
  });

  it('should compare by bed', function(){
    first.location[0].bed = "2";
    second.location[0].bed = "1";
    expect(first.compare(second, LocationWardComparator)).toEqual(1);
  });
});
