"""
Plugin definition
"""
from opal.core import plugins, episodes

from walkin.urls import urlpatterns

class WalkinPlugin(plugins.OpalPlugin):
    urls = urlpatterns
    javascripts = {
        'opal.controllers': [
            'js/walkin/controllers/walkin_hospital_number.js',
            'js/walkin/controllers/walkin_discharge.js',
            'js/walkin/controllers/nurse_investigation.js',
            'js/walkin/controllers/zika.js'
        ]
    }
    actions = [
        'actions/walkin_next.html',
        'actions/nurse_investigations.html',
        'actions/discharge_summary.html',
        'actions/zika_patient.html'
    ]


class WalkinEpisode(episodes.EpisodeType):
    name            = 'Walkin'
    detail_template = 'detail/walkin.html'


plugins.register(WalkinPlugin)
