"""
Discharge summary template for Walkin
"""
from dischargesummary import DischargeTemplate

class WalkinDoctorDischargeLetter(DischargeTemplate):
    name = 'walkindoctor'
    template = 'walkin_discharge_letter.html'
    button_display = 'Clinic Letter'


class WalkinNurseDischargeLetter(DischargeTemplate):
    name = 'walkinnurse'
    template = 'walkin_nurse_discharge_letter.html'
    button_display = 'Nurse Clinic Letter'
