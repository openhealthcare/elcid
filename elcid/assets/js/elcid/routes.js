var app = angular.module('opal');
app.config(
    ['$routeProvider',
     function($routeProvider){
	     $routeProvider.when('/',  {
            controller: 'WelcomeCtrl',
            controllerAs: 'welcome',
            templateUrl: '/templates/welcome.html',
            resolve: {
              options: function(Options) { return Options; },
            },
        });
     }]);
