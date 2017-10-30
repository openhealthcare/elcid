module.exports = function(config){
  // var opalPath;
  // if(process.env.TRAVIS){
  //   // the python version from travis return 2.7, but the env its using is 2.7
  //   // python_version = process.env.TRAVIS_PYTHON_VERSION;
  //   python_version = "2.7.13";
  //   opalPath = '/home/travis/virtualenv/python' + python_version + '/src/opal';
  // }
  // else{
  //   opalPath = '../../opal';
  // }
  // var karmaDefaults = require(opalPath + '/config/karma_defaults.js');
  var karmaDefaults = require("../config/karma_defaults.js");
  var baseDir = __dirname + '/..';
  var coverageFiles = [
    __dirname + '/../elcid/assets/js/elcid/*',
    __dirname + '/../elcid/assets/js/elcid/controllers/*',
    __dirname + '/../elcid/assets/js/elcid/services/*',
    __dirname + '/../elcid/assets/js/elcid/services/records/*',
    __dirname + '/../opat/static/js/opat/controllers/*',
    __dirname + '/../walkin/static/js/walkin/controllers/*',
    __dirname + '/../infectiousdiseases/static/js/infectiousdiseases/controllers/*.js',
  ];
  var includedFiles = [
    'opal/app.js',
    // Our application

    __dirname + '/../elcid/assets/js/elcid/*.js',
    __dirname + '/../elcid/assets/js/elcid/controllers/*.js',
    __dirname + '/../elcid/assets/js/elcid/services/*.js',
    __dirname + '/../elcid/assets/js/elcid/services/records/*.js',
    __dirname + '/../opat/static/js/opat/controllers/*.js',
    __dirname + '/../research/static/js/research/controllers/*.js',
    __dirname + '/../walkin/static/js/walkin/controllers/*.js',
    __dirname + '/../infectiousdiseases/static/js/infectiousdiseases/controllers/*.js',


    // The tests
    __dirname + '/../elcid/assets/js/elcidtest/*.js',
    __dirname + '/../opat/static/js/test/*.js',
    __dirname + '/../research/static/js/test/*.js',
      __dirname + '/../walkin/static/js/walkintest/*.js',
    __dirname + '/../infectiousdiseases/static/js/infectiousdiseasestest/*.js',

  ];

  var defaultConfig = karmaDefaults(includedFiles, baseDir, coverageFiles);
  config.set(defaultConfig);
};
