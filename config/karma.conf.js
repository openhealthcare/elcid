module.exports =  function(config){
    var browsers, basePath, coverageReporter;
    var additionalDependencies;

    if(process.env.TRAVIS){
        browsers = ["Firefox"];
        basePath = '/home/travis/virtualenv/python2.7/src/opal/opal/static/js';
        coverageReporter = {
            type: 'lcovonly', // lcov or lcovonly are required for generating lcov.info files
            dir: __dirname + '/../coverage/',
        };
        additionalDependencies = require('/home/travis/virtualenv/python2.7/src/opal/config/karma_dependencies.js');
    }
    else{
        browsers = ['PhantomJS'];
        basePath = '../../opal/opal/static/js';
        coverageReporter = {
            type : 'html',
            dir : __dirname + '/../htmlcov/js/'
        };
        additionalDependencies = require('../../opal/config/karma_dependencies.js');
    }

    var preprocessors = {};
    preprocessors[__dirname + '/../elcid/assets/js/elcid/*'] = 'coverage';
    preprocessors[__dirname + '/../elcid/assets/js/elcid/controllers/*'] = 'coverage';
    preprocessors[__dirname + '/../elcid/assets/js/elcid/services/*'] = 'coverage';
    preprocessors[__dirname + '/../elcid/assets/js/elcid/services/records/*'] = 'coverage';
    preprocessors[__dirname + '/../opat/static/js/opat/controllers/*'] = 'coverage';
    preprocessors[__dirname + '/../walkin/static/js/walkin/controllers/*'] = 'coverage';

    config.set({
        frameworks: ['jasmine'],
        browsers: browsers,
        basePath:  basePath,

        files: additionalDependencies().concat([
          'opal/app.js',
          // Our application

          __dirname + '/../elcid/assets/js/elcid/*.js',
          __dirname + '/../elcid/assets/js/elcid/controllers/*.js',
          __dirname + '/../elcid/assets/js/elcid/services/*.js',
          __dirname + '/../elcid/assets/js/elcid/services/records/*.js',
          __dirname + '/../opat/static/js/opat/controllers/*.js',
          __dirname + '/../research/static/js/research/controllers/*.js',
          __dirname + '/../walkin/static/js/walkin/controllers/*.js',


          // The tests
          __dirname + '/../elcid/assets/js/elcidtest/*.js',
          __dirname + '/../opat/static/js/test/*.js',
          __dirname + '/../research/static/js/test/*.js',
          __dirname + '/../walkin/static/js/walkintest/*.js',
        ]),

        preprocessors: preprocessors,

        reporters: ['progress', 'coverage'],
        autoWatch: true,

        coverageReporter: coverageReporter,

        // Stolen from http://oligofren.wordpress.com/2014/05/27/running-karma-tests-on-browserstack/
        browserDisconnectTimeout : 10000, // default 2000
        browserDisconnectTolerance : 1, // default 0
        browserNoActivityTimeout : 4*60*1000, //default 10000
        captureTimeout : 4*60*1000, //default 60000
    });
}
