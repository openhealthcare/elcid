"""
Plugin definition
"""
from django.conf import settings

from opal.core import plugins
from opal.utils import camelcase_to_underscore, stringport

from wardround.urls import urlpatterns

# So we only do it once
IMPORTED_FROM_APPS = False

def import_from_apps():
    """
    Iterate through installed apps attempting to import app.wardrounds
    This way we allow our implementation, or plugins, to define their
    own ward rounds.
    """
    print "Importing from apps"
    for app in settings.INSTALLED_APPS:
        try:
            stringport(app + '.wardrounds')
        except ImportError:
            pass # not a problem
    global IMPORTED_FROM_APPS
    IMPORTED_FROM_APPS = True
    return


class WardRoundsPlugin(plugins.OpalPlugin):
    """
    Main entrypoint to expose this plugin to the host
    OPAL instance !
    """
    urls = urlpatterns
    javascripts = {
        'opal.wardround': [
            'js/wardround/app.js',
            'js/wardround/services/ward_round_loader.js',
            'js/wardround/controllers/list.js',
            'js/wardround/controllers/wardround.js',
            'js/wardround/controllers/episode_detail.js',
            'js/wardround/controllers/find_patient.js',
        ]
    }
    menuitems = [
        dict(
            href="/wardround/#/", display="Ward Rounds", icon="fa fa-tasks",
            activepattern='/wardround', index=1)
    ]


plugins.register(WardRoundsPlugin)

class BaseWardRound(object):
    """
    Ward round utility methods - shouldn't have to override these !
    """
    name        = None
    description = None

    @classmethod
    def get(klass, name):
        """
        Return a specific ward round by slug
        """
        if not IMPORTED_FROM_APPS:
            import_from_apps()

        for sub in klass.__subclasses__():
            if sub.slug() == name:
                return sub

    @classmethod
    def list(klass):
        """
        Return a list of all ward rounds
        """
        if not IMPORTED_FROM_APPS:
            import_from_apps()
        return klass.__subclasses__()

    @classmethod
    def slug(klass):
        return camelcase_to_underscore(klass.name).replace(' ', '')


class WardRound(BaseWardRound):
    """
    Base Ward Round class - individual wardrounds should override this.
    """
    name        = 'PLEASE NAME ME Larry!'
    description = 'PLEASE DESCRIBE ME Larry!'

    detail_template = 'detail/wardround_default.html'
    filter_template = None
    filters         = {}

    @staticmethod
    def episodes():
        """
        Subclasses should override this method in order to define a getter
        method that returns an iterable of opal.models.Episode instances
        that are 'on' this ward round.
        """
        return []

    @classmethod
    def to_dict(klass, user):
        """
        If you need to change the way episodes are serialised - e.g. to insert
        extra data, subclassing this method would be a good place to do it!
        """
        from opal.models import Episode

        return dict(name=klass.name,
                    description=klass.description,
                    episodes=Episode.objects.serialised(user, klass.episodes(),
                                                        episode_history=True),
                    filters=klass.filters)
