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
    __dirname + '/../microhaem/static/js/haem/controllers/*',
    __dirname + '/../walkin/static/js/walkin/controllers/*',
    __dirname + '/../research/static/js/research/controllers/*.js',
    // __dirname + '/../search/static/js/search/*',
    __dirname + '/../infectiousdiseases/static/js/infectiousdiseases/controllers/*.js',
  ];
  var includedFiles = [
    'opal/app.js',
    // Our application
    // The tests
    __dirname + '/../elcid/assets/js/elcidtest/*.js',
    __dirname + '/../opat/static/js/test/*.js',
    __dirname + '/../research/static/js/test/*.js',
    __dirname + '/../microhaem/static/js/test/*.js',
    __dirname + '/../walkin/static/js/walkintest/*.js',
    // __dirname + '/../search/static/js/test/*.js',
    __dirname + '/../infectiousdiseases/static/js/infectiousdiseasestest/*.js',
    '../../core/pathway/static/js/pathway/**/*.js',

  ].concat(coverageFiles);

  var defaultConfig = karmaDefaults(includedFiles, baseDir, coverageFiles);
  config.set(defaultConfig);
};
