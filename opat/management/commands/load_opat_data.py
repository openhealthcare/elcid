from datetime import datetime, date, timedelta
from django.utils import timezone

NOW = timezone.now()

TODAY = NOW.date()

Demographics = [
    'external_system',
    'external_identifier',
    'patient_id',
    'hospital_number',
    'nhs_number',
    'surname',
    'first_name',
    'middle_name',
    'date_of_birth',
    'religion',
    'date_of_death',
    'post_code',
    'gp_practice_code',
    'death_indicator',
    'title',
    'marital_status',
    'sex',
    'birth_place',
    'ethnicity'
 ]
Location = [
    'episode_id',
    'category',
    'hospital',
    'ward',
    'bed',
    'opat_referral_route',
    'opat_referral_team',
    'opat_referral_consultant',
    'opat_referral_team_address',
    'opat_referral',
    'opat_acceptance',
    'opat_discharge'
]
Diagnosis = [
    'episode_id', 'provisional', 'details', 'date_of_diagnosis', u'condition'
]
PastMedicalHistory = [
    'episode_id', 'year', 'details', 'condition'
]

Antimicrobial = [
    'episode_id',
    'dose',
    'start_date',
    'end_date',
    'comments',
    'no_antimicrobials',
    'frequency',
    'drug',
    'delivered_by',
    'adverse_event',
    'reason_for_stopping',
    'route
]
MicrobiologyTest = [
    'episode_id',
    'test',
    'date_ordered',
    'details',
    'microscopy',
    'organism',
    'sensitive_antibiotics',
    'resistant_antibiotics',
    'result',
    'igm',
    'igg',
    'vca_igm',
    'vca_igg',
    'ebna_igg',
    'hbsag',
    'anti_hbs',
    'anti_hbcore_igm',
    'anti_hbcore_igg',
    'rpr',
    'tppa',
    'viral_load',
    'parasitaemia',
    'hsv',
    'vzv',
    'syphilis',
    'c_difficile_antigen',
    'c_difficile_toxin',
    'species',
    'hsv_1',
    'hsv_2',
    'enterovirus',
    'cmv',
    'ebv',
    'influenza_a',
    'influenza_b',
    'parainfluenza',
    'metapneumovirus',
    'rsv',
    'adenovirus',
    'norovirus',
    'rotavirus',
    'giardia',
    'entamoeba_histolytica',
    'cryptosporidium',
    'rhinovirus',
    'alert_investigation',
    'spotted_fever_igm',
    'spotted_fever_igg',
    'typhus_group_igm',
    'typhus_group_igg',
    'scrub_typhus_igm',
    'scrub_typhus_igg',
    'hiv_declined'
]
OPATReview = [
    'episode_id',
    'datetime',
    'initials',
    'discussion',
    'opat_plan',
    'next_review',
    'dressing_changed',
    'bung_changed',
    'medication_administered',
    'adverse_events',
    'rv_type'
]

Line = [
    u'episode_id',
    'insertion_datetime',
    'inserted_by',
    'external_length',
    'removal_datetime',
    'special_instructions',
    'site',
    'line_type',
    'removal_reason',
    'complications'
]
OPATOutstandingIssues = [
    'episode_id', 'details'
]
OPATOutcome = [
    u'episode_id',
    'outcome_stage',
    'treatment_outcome',
    'patient_outcome',
    'opat_outcome',
    'deceased',
    'death_category',
    'cause_of_death',
    'readmitted',
    'readmission_cause',
    'notes',
    'patient_feedback',
    'infective_diagnosis'
]

ContactDetails = [
    u'patient_id',
    'address_line1',
    'address_line2',
    'city',
    'county',
    'post_code',
    'tel1',
    'tel2'
]
Carers = [
    u'patient_id', 'gp', 'nurse'
]
Allergies = [
    'external_system',
    'external_identifier',
    u'patient_id',
    'provisional',
    'details',
    'allergy_description',
    'allergy_type_description',
    'certainty_id',
    'certainty_description',
    'allergy_reference_name',
    'allergen_reference_system',
    'allergen_reference',
    'status_id',
    'status_description',
    'diagnosis_datetime',
    'allergy_start_datetime',
    'no_allergies',
    'drug'
]
Observations = [
    u'episode_id',
    'bp_systolic',
    'bp_diastolic',
    'pulse',
    'resp_rate',
    'sp02',
    'temperature',
    'height',
    'weight',
    'datetime'
]
Travel = [
    u'episode_id',
    'dates',
    'did_not_travel',
    'specific_exposures',
    'malaria_prophylaxis',
    'malaria_compliance',
    'malaria_drug',
    'destination',
    'reason_for_travel'
]
Appointment = [
    u'episode_id', 'appointment_type', 'appointment_with', 'date'
]
MicrobiologyInput = [
    u'episode_id',
    'when',
    'initials',
    'clinical_discussion',
    'agreed_plan',
    'discussed_with',
    'clinical_advice_given',
    'infection_control_advice_given',
    'change_in_antibiotic_prescription',
    'referred_to_opat',
    'reason_for_interaction'
]
OPAT Line Assessment = [
    u'episode_id',
    'line',
    'assessment_date',
    'vip_score',
    'dressing_type',
    'dressing_change_date',
    'dressing_change_reason',
    'next_bionector_date',
    'bionector_change_date',
    'comments',
    'dressing_intact',
    'lumen_flush_ok',
    'blood_drawback_seen',
    'cm_from_exit_site'
]

patient_1 = dict(
    demographics={
        hospital_number="1231212123",
        first_name="David",
        surname="ABBOT",
        date_of_birth=date(1980, 10, 21)
    },
    location=dict(
        category="OPAT",
        opat_referral=TODAY - timedelta(10),
        opat_referral_consultant="Gardner",
        opat_referral_team="Urological Surgery"
    ),
    diagnosis=[dict(
        condition="ESBL bacteraemia",
        details="recurrance",
        date_of_diagnosis=TODAY - timedelta(10)
    )],
    past_medical_history=[
        dict(
            condition="stent right urethra",
            year="September 2018"
        ),

    ],
    antimicrobial=[dict(
        drug="Ertapenem",
        start_date=TODAY - timedelta(7),
        dose="1g",
        route="IV",
        frequency="Once a day",
        delivered_by="Inpatient Team"
    )],
    microbiology_test=[
        dict(
            test="VTE Assessment"
        ),
        dict(
            test="MRSA PCR"
        )
    ],
    opat_review=[
        dict(
            initals="W Chung",
            opat_plan="No plans to discharge, continuing investigation required",
            datetime=NOW - timedelta(1)
        ),
        dict(
            initals="P Wall",
            opat_plan="Dicharge date confirmed, waiting for bloods",
            datetime=NOW - timedelta(4)
        ),
        dict(
            initals="W Chung",
            opat_plan="""
1. Needs OPAT appt
2. Equipment list to ward
"""
            datetime=NOW - timedelta(6)
        ),
        dict(
            initals="W Chung",
            opat_plan="""
Received call from urology team, planning discharge tomorrow
PICC line due tomorrow morning
DN visit planned on Wednesday
Need to give equipment list to ward
""",
            datetime=NOW - timedelta(7)
        )
    ],
    opat_outstanding_issues=[
        dict(
            details="Follow up appt",
        ),
        dict(
            details="Update meds",
            opat_plan="""
1. Referral sent to DNs for 1st visit, a/w reply:apprently according to OPAT nurs DNs will see patients with a cannula
2. Provisional discharge summary sent
3. PICC line planned for tomorrow morning @ 10:30
""",
            datetime=NOW - timedelta(7)
        )
    ]

)