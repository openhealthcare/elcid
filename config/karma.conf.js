module.exports = function(config){
  var opalPath;
  if(process.env.TRAVIS){
    python_version = process.env.TRAVIS_PYTHON_VERSION;
    opalPath = '/home/travis/virtualenv/python' + python_version + '/src/opal';
  }
  else{
    opalPath = '../../opal';
  }
  var karmaDefaults = require(opalPath + '/config/karma_defaults.js');
  var karmaDir = __dirname;
  var coverageFiles = [
    __dirname + '/../elcid/assets/js/elcid/*',
    __dirname + '/../elcid/assets/js/elcid/controllers/*',
    __dirname + '/../elcid/assets/js/elcid/services/*',
    __dirname + '/../elcid/assets/js/elcid/services/records/*',
    __dirname + '/../opat/static/js/opat/controllers/*',
    __dirname + '/../walkin/static/js/walkin/controllers/*'
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


    // The tests
    __dirname + '/../elcid/assets/js/elcidtest/*.js',
    __dirname + '/../opat/static/js/test/*.js',
    __dirname + '/../research/static/js/test/*.js',
    __dirname + '/../walkin/static/js/walkintest/*.js'
  ];

  var defaultConfig = karmaDefaults(karmaDir, coverageFiles, includedFiles);
  config.set(defaultConfig);
};
