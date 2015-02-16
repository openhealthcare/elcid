"""
Referral routes for elCID
"""
from referral import ReferralRoute

class HTDWalkInRoute(ReferralRoute):
    name = 'HTD Walk In Clinic'
    description = 'The HTD Walk-In clinic provides a primary care service to returning travelers.'
    target_teams = ['walkin', 'walkin_triage']
    target_category = 'Walkin'
    success_link = '/#/list/walkin'

