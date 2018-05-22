//
// Main Elcid Search Angular application
//
!(function(){
  var opal = OPAL.module('opal');
  var app = OPAL.module('opal.search', [
      'ngRoute',
      'ngProgressLite',
      'ngCookies',
      'opal.filters',
      'opal.services',
      'opal.directives',
      'opal.controllers'
  ]);

  OPAL.run(app);

  app.config(function($routeProvider){
    $routeProvider
    .when('/', {
      controller: 'SearchCtrl',
      templateUrl: '/search/templates/search.html',
    })
    .when('/extract/:extractFilterId', {
        controller: 'ExtractCtrl',
        templateUrl: '/search/templates/extract.html',
        resolve: {
          profile: function(UserProfile){ return UserProfile.load(); },
          extractQuerySchema: function(extractQuerySchemaLoader){ return extractQuerySchemaLoader.load(); },
          extractSliceSchema: function(extractSliceSchemaLoader){ return extractSliceSchemaLoader.load(); },
          extractQuery: function(extractQueryLoader, $route){
            return extractQueryLoader.load($route.current.params.extractFilterId);
          },
          referencedata: function(Referencedata){ return Referencedata.load(); }
        }
    })
    .when('/extract', {
        controller: 'ExtractCtrl',
        templateUrl: '/search/templates/extract.html',
        resolve: {
          extractQuerySchema: function(extractQuerySchemaLoader){ return extractQuerySchemaLoader.load(); },
          extractSliceSchema: function(extractSliceSchemaLoader){ return extractSliceSchemaLoader.load(); },
          extractQuery: function(){ return null; },
          referencedata: function(Referencedata){ return Referencedata.load(); }
        }
    })
  });
})();
