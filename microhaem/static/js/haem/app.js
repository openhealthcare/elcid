var opal = OPAL.module('opal');
var app = OPAL.module('haem.referrals', [
    'ngRoute',
    'ngProgressLite',
    'ngCookies',
    'opal.filters',
    'opal.services',
    'opal.directives',
    'opal.controllers',
]);
OPAL.run(app);
