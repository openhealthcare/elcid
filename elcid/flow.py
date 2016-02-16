"""
Defining the patient flows for our system.
"""
diagnosis_flow = {
    'enter': {
        'controller': 'DiagnosisHospitalNumberCtrl',
        'template'  : '/templates/modals/hospital_number.html/'
    },
    'exit': {
        'controller': 'DiagnosisDischargeCtrl',
        'template'  : '/templates/elcid/modals/diagnosis_discharge.html'
    }
}


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
    'infectious_diseases': {
        'id_inpatients': diagnosis_flow
    },
    'hiv': {
        'immune_inpatients': diagnosis_flow
    },
    'tropical_diseases': {
        'default': diagnosis_flow

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
flows['Walkin'] = flows['walkin']['default'] # Episode Category
