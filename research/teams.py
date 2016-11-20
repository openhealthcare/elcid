# """
# research study teams!
# """
# #from opal.models import Team

# def get_study_teams(user):
#     """
#     Given a USER, return a list of study teams that this user can see.

#     If USER is not authenticated, just return []
#     """
#     # This has to be here because Django wants to make sure it's the first
#     # thing to import models and gets distinctly snippish if you beat it.
#     from research.models import ResearchStudy

#     #    Go through study roles, getting those for which this user is that role.
#     teams = []

#     if not user.is_authenticated():
#         return teams

#     clinical_leads = user.clinical_lead_user.all()
#     if clinical_leads:
#         for study in clinical_leads:
#             study_team = Team.objects.get(name=study.team_name)
#             other_teams = Team.objects.filter(parent=study_team)
#             teams.append(study_team)
#             teams += list(other_teams)

#     researchers = user.researcher_user.all()
#     if researchers:
#         for study in researchers:
#             print study.team_name
#             study_team = Team.objects.get(name=study.team_name)
#             teams.append(study_team)
#             teams.append(Team.objects.get(parent=study_team,
#                                           name=study.team_name + '_research_practitioner'))
#             teams.append(Team.objects.get(parent=study_team,
#                                           name=study.team_name + '_scientist'))

#     research_nurses = user.research_nurse_user.all()
#     if research_nurses:
#         for study in research_nurses:
#             study_team = Team.objects.get(name=study.team_name)
#             teams.append(study_team)
#             teams.append(Team.objects.get(parent=study_team,
#                                           name=study.team_name + '_research_practitioner'))

#     scientists = user.scientist_user.all()
#     if scientists:
#         for study in scientists:
#             study_team = Team.objects.get(name=study.team_name)
#             teams.append(study_team)
#             teams.append(Team.objects.get(parent=study_team,
#                                           name=study.team_name + '_scientist'))

#     return list(set(teams))
