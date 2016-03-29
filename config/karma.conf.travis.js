module.exports =  function(config){
    var preprocessors = {};
    preprocessors[__dirname + '/../elcid/assets/js/elcid/*'] = 'coverage';
    preprocessors[__dirname + '/../elcid/assets/js/elcid/controllers/*'] = 'coverage';
    preprocessors[__dirname + '/../elcid/assets/js/elcid/services/*'] = 'coverage';
    preprocessors[__dirname + '/../opat/static/js/opat/controllers/*'] = 'coverage';
    preprocessors[__dirname + '/../research/static/js/research/controllers/*'] = 'coverage';
    preprocessors[__dirname + '/../walkin/static/js/walkin/controllers/*'] = 'coverage';

    config.set({
        frameworks: ['jasmine'],
        browsers: ['Firefox'],
        basePath:  '/home/travis/virtualenv/python2.7/src/opal/opal/static/js',

        files: [
            //JASMINE,
            //JASMINE_ADAPTER,
            'angular-1.2.20/angular.js',
            'angular-1.2.20/angular-route.js',
            'angular-1.2.20/angular-resource.js',
            'angular-1.2.20/angular-cookies.js',
            'angular-1.2.20/angular-mocks.js',

            'angular-ui-utils-0.1.0/ui-utils.js',
            'angular-ui-bootstrap-0.10.0/ui-bootstrap-tpls.js',
            'angular-strap-2.3.1/angular-strap.js',
            'angular-strap-2.3.1/modules/compiler.js',
            'angular-strap-2.3.1/modules/tooltip.js',
            'angular-strap-2.3.1/modules/tooltip.tpl.js',
            'angular-strap-2.3.1/modules/dimensions.js',
            'angular-strap-2.3.1/modules/parse-options.js',
            'angular-strap-2.3.1/modules/date-parser.js',
            'angular-strap-2.3.1/modules/datepicker.js',
            'angular-strap-2.3.1/modules/datepicker.tpl.js',
            'angular-strap-2.3.1/modules/timepicker.js',
            'angular-strap-2.3.1/modules/timepicker.tpl.js',
            'angular-strap-2.3.1/modules/typeahead.js',
            'angular-strap-2.3.1/modules/typeahead.tpl.js',
            "angulartics-0.17.2/angulartics.min.js",
            "angulartics-0.17.2/angulartics-ga.min.js",
            'ngprogress-lite/ngprogress-lite.js',
            'jquery-1.11.3/jquery-1.11.3.js',
            'utils/underscore.js',
            'utils/moment.js',
            'bower_components/angular-growl-v2/build/angular-growl.js',
            'bower_components/ment.io/dist/mentio.js',
            'bower_components/ment.io/dist/templates.js',
            'bower_components/angular-ui-select/dist/select.js',
            "bower_components/angular-local-storage/dist/angular-local-storage.js",
            'opal/utils.js',
            'opal/directives.js',
            'opal/filters.js',
            'opal/services_module.js',
            'opal/services/*.js',
            'opal/controllers_module.js',
            'opal/controllers/*.js',
            'opal/app.js',
            '../../core/search/static/js/search/controllers/*',
            '../../core/search/static/js/search/services/*',


            // Our application

            __dirname + '/../elcid/assets/js/elcid/*',
            __dirname + '/../elcid/assets/js/elcid/controllers/*',
            __dirname + '/../elcid/assets/js/elcid/services/*',
            __dirname + '/../opat/static/js/opat/controllers/*',
            __dirname + '/../research/static/js/research/controllers/*',
            __dirname + '/../walkin/static/js/walkin/controllers/*',


            // The tests
            __dirname + '/../elcid/assets/js/elcidtest/*.js',
            // '../../../../elcid/opat/static/js/test/*',
            // '../../../../elcid/research/static/js/test/*',
            __dirname + '/../elcid/walkin/static/js/walkintest/*.js',
        ],

        preprocessors: preprocessors,

        reporters: ['progress', 'coverage'],
        singleRun: true,
        autoWatch: true,

        coverageReporter: {
            type : 'lcovonly',
            dir : __dirname + '/../coverage/',
        },

        // Stolen from http://oligofren.wordpress.com/2014/05/27/running-karma-tests-on-browserstack/
        browserDisconnectTimeout : 10000, // default 2000
        browserDisconnectTolerance : 1, // default 0
        browserNoActivityTimeout : 4*60*1000, //default 10000
        captureTimeout : 4*60*1000, //default 60000
    })
}
