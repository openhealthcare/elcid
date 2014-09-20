"""
Defining the patient flows for our system.
"""

flows = {
    'default': {
        'enter': {
            'controller': 'HospitalNumberCtrl',
            'template'  : '/templates/modals/hospital_number.html/'
        },
        'exit': {
            'controller': 'ElcidDischargeEpisodeCtrl',
            'template'  : '/templates/modals/discharge_episode.html/'
        }
    },
    'opat': {
        'default': {
            'enter': {
                'controller': 'OPATReferralCtrl',
                'template'  : '/templates/modals/opat_referral.html/'
            },
            'exit': {
                'controller': 'OPATDischargeCtrl',
                'template'  : '/templates/modals/discharge_opat_episode.html/'
            }
        }
    },
    'infectious_diseases': {
        'id_inpatients': {
            'enter': {
                'controller': 'DiagnosisHospitalNumberCtrl',
                'template'  : '/templates/modals/hospital_number.html/'
            }
        }
    },
    'hiv': {
        'immune_inpatients': {
            'enter': {
                'controller': 'DiagnosisHospitalNumberCtrl',
                'template'  : '/templates/modals/hospital_number.html/'
            }
        }
    },
    'tropical_diseases': {
        'default': {
            'enter': {
                'controller': 'DiagnosisHospitalNumberCtrl',
                'template'  : '/templates/modals/hospital_number.html/'
            }
        }
    },
    'walkin': {
        'default': {
            'enter': {
                'controller': 'WalkinHospitalNumberCtrl',
                'template'  : '/templates/modals/hospital_number.html/'
            },
            'exit': {
                'controller': 'WalkinDischargeCtrl',
                'template'  : '/templates/modals/discharge_walkin_episode.html/'
            }
        }
    }
}
