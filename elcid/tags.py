from opal.utils import Tag

TAGS = [
    Tag('microbiology', 'Micro', [
            Tag('micro_ortho', 'Micro-Ortho', None),
            Tag('micro_icu', 'Micro-ICU', None),
            Tag('micro_haem', 'Micro-Haem', None),
            Tag('micro_tower_review', 'Tower Review', None),
            Tag('micro_handover', 'Micro-C diff 2014', None),
            Tag('micro_c_diff_new', 'Micro-C diff NEW', None),
            Tag('micro_c_diff_review', 'Micro-C diff REVIEW', None),
            ]),
    Tag('infectious_diseases', 'ID', [
            Tag('id_inpatients', 'ID Inpatients', None),
            Tag('id_liaison', 'ID Liaison', None)
            ]),
    Tag('hiv', 'Immune', [
            Tag('immune_inpatients', 'Immune Inpatients', None),
            Tag('immune_liason', 'Immune Liason', None)
            ]),
    Tag('tropical_diseases', 'Tropical', None),
    Tag('virology', 'Virology', None),
    Tag('mine', 'Mine', None),
]
