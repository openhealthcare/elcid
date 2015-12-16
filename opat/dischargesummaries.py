"""
Discharge summary template for OPAT
"""
from dischargesummary import DischargeTemplate

class OPATDischargeLetter(DischargeTemplate):
    name = 'opat'
    template = 'opat_discharge_letter.html'
    button_display = 'OPAT Letter'
