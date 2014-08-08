"""
Defining the patient flows for our system.
"""

flows = {
    'default': {
        'enter': {
            'controller': 'HospitalNumberCtrl',
            'template'  : '/templates/modals/hospital_number.html/'
            },
        'exit': 'DischargeEpisodeCtrl'
    }
}
