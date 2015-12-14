"""
Template tags for [Virtual] Ward Rounds
"""
from django import template

register = template.Library()

@register.inclusion_tag('wardround/partials/team_filter.html',
                        takes_context=True)
def team_filter(context):
    teams = context['request'].user.profile.get_teams()
    teams = sorted(teams, key=lambda t: t.name)
    return {'teams': teams }
