from django.test import TestCase
from mock import MagicMock

from opal.models import Team

from wardround.templatetags.wardrounds import team_filter

class TeamFilterTestCase(TestCase):
    def test_team_filter_alphebetises(self):
        wat = Team(name='wat')
        bar = Team(name='bar')
        baz = Team(name='baz')
        caz = Team(name='caz')
        context = MagicMock()
        context['request'].user.profile.get_teams.return_value = [wat, bar, caz, baz]
        teams = team_filter(context)
        expected = ['bar', 'baz', 'caz', 'wat']
        self.assertEqual([t.name for t in teams['teams']], expected)
