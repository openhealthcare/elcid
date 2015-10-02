var app = angular.module('opal');
app.config(
    ['$routeProvider',
     function($routeProvider){
	     $routeProvider.when('/',  {
            controller: 'WelcomeCtrl',
            templateUrl: '/templates/welcome.html'
        });
     }]);
