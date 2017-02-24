//
// Service for locating controllers and templates for
//
angular.module('opal.services').factory('elCIDFlow', function($routeParams){
    "use strict";

    var data_collection_slugs = [
        'hiv-immune_inpatients',
        'infectious_diseases-id_inpatients',
        'tropical_diseases'
    ];

    var categories = {
        'Walkin': {
            enter: function(){
                return {
                    'controller': 'WalkinHospitalNumberCtrl',
                    'template'  : '/templates/modals/hospital_number.html/'
                };
            },
            exit: function(episode){
                return {
                    'controller': 'WalkinDischargeCtrl',
                    'template'  : '/templates/modals/discharge_walkin_episode.html/'
                };
            }
        },
        'Inpatient': {
            enter: function(){
                if($routeParams.slug && data_collection_slugs.indexOf($routeParams.slug) != -1){
                    return {
                        'controller': 'DiagnosisHospitalNumberCtrl',
                        'template'  : '/templates/modals/hospital_number.html/'
                    }
                }
                if($routeParams.slug && $routeParams.slug === 'virology'){
                  return {
                      'controller': 'VirologyHospitalNumberCtrl',
                      'template'  : '/templates/modals/hospital_number.html/'
                  }
                }
                return {
                    'controller': 'HospitalNumberCtrl',
                    'template'  : '/templates/modals/hospital_number.html/'
                }
            },
            exit: function(episode){
                if($routeParams.slug && data_collection_slugs.indexOf($routeParams.slug) != -1){
                    return {
                        'controller': 'DiagnosisDischargeCtrl',
                        'template'  : '/templates/elcid/modals/diagnosis_discharge.html'
                    }
                }

                return {
                    'controller': 'ElcidDischargeEpisodeCtrl',
                    'template'  : '/templates/modals/discharge_episode.html/'
                }

            }
        },
        'OPAT': {
            enter: function(){
                return {
                    'controller': 'OPATReferralCtrl',
                    'template'  : '/opat/templates/modals/opat_referral.html/'
                }
            },
            exit: function(episode){
                return {
                    'controller': 'OPATDischargeCtrl',
                    'template'  : '/opat/templates/modals/discharge_opat_episode.html/'
                }
            }
        },
        TropicalLiaison: {
            enter: function(){
                return {
                    controller: "TropicalLiaisonAddPatient",
                    template: '/templates/infectiousdiseases/tropical_liaison_admission.html'
                }
            },
            exit: function(episode){
                return {
                    'controller': 'ElcidDischargeEpisodeCtrl',
                    'template'  : '/templates/infectiousdiseases/tropical_liaison_discharge.html'
                }
            }
        }
    }

    var Flow = {
        enter: function(){
            var episode_type = 'Inpatient';
            if($routeParams.slug){
                if($routeParams.slug.indexOf('opat') == 0){
                    episode_type = 'OPAT';
                }else if ($routeParams.slug.indexOf('walkin') == 0){
                    episode_type = 'Walkin';
                }
                else if($routeParams.slug === 'tropical_liaison'){
                    episode_type = 'TropicalLiaison';
                }
            }
            return categories[episode_type]['enter']();
        },
        exit: function(episode){
            if($routeParams.slug === 'tropical_liaison'){
              return categories.TropicalLiaison.exit(episode);
            }
            return categories[episode.category_name]['exit'](episode);
        }
    }
    return Flow
})
