module.exports = function(config){
  var opalPath = process.env.OPAL_LOCATION;
  var karmaDefaults = require(opalPath + '/opal/tests/js_config/karma_defaults.js');
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
