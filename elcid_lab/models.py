from lab import models as lmodels
from opal.utils import AbstractBase


class ElcidLabTest(lmodels.LabTest, AbstractBase):
    additional_information = lmodels.GenericInput(verbose_name="Details")


class PosNegEquivicalNotDoneTest(ElcidLabTest, AbstractBase):
    result = lmodels.PosNegEquivicalNotDone()


class AmoebicSerology(PosNegEquivicalNotDoneTest):
    _title = "Amoebic Serology"


class CystercicosisSerology(PosNegEquivicalNotDoneTest):
    _title = "Cystercicosis Serology"


class FasciolaSerology(PosNegEquivicalNotDoneTest):
    _title = "Fasciola Serology"


class FilariaSerology(PosNegEquivicalNotDoneTest):
    _title = "Filaria Serology"


class HydatidSerology(PosNegEquivicalNotDoneTest):
    _title = "Hydatid Serology"


class StrongyloidesSerology(PosNegEquivicalNotDoneTest):
    _title = "Strongyloides Serology"


class ToxcocaraSerology(PosNegEquivicalNotDoneTest):
    _title = "Toxcocara Serology"


class TBruceiSerology(PosNegEquivicalNotDoneTest):
    _title = "T brucei Serology"
    _synonyms = ["Trypanosomiasis brucei Serology"]


class TCruziSerology(PosNegEquivicalNotDoneTest):
    _title = "T cruzi serolog"


class SchistosomaSerology(PosNegEquivicalNotDoneTest):
    _title = "Schistosoma serology"


class LeishmaniaSerology(PosNegEquivicalNotDoneTest):
    _title = "Leishmania serology"


class TrichinellaSerology(PosNegEquivicalNotDoneTest):
    _title = "Trichinella serology"


class HIVPointOfCare(PosNegEquivicalNotDoneTest):
    _title = "HIV Point of Care"


class StoolParasitologyPCR(ElcidLabTest):
    _title = "Stool Parasitology PCR"

    giardia = lmodels.PendingPosNeg()
    entamoeba_histolytica = lmodels.PendingPosNeg(
        verbose_name="Entamoeba Histolytica"
    )
    cryptosporidium = lmodels.PendingPosNeg()


class RespiratoryVirusPCR(ElcidLabTest):
    _title = "Respiratory Virus PCR"
    _synonyms = ["Viral Throat Swab", "Flu swab"]
    influenza_a = lmodels.PendingPosNeg()
    influenza_b = lmodels.PendingPosNeg()
    parainfluenza = lmodels.PendingPosNeg()
    metapneumovirus = lmodels.PendingPosNeg()
    rsv = lmodels.PendingPosNeg()
    adenovirus = lmodels.PendingPosNeg()


class Cdiff(ElcidLabTest):
    _title = "C diff"
    _synonyms = ["Clostridium difficile"]
    c_difficile_antigen = lmodels.PendingPosNeg(
        verbose_name="C. difficile antigen"
    )
    c_difficile_toxin = lmodels.PendingPosNeg(
        verbose_name="C. difficile toxin"
    )


class Parasitaemia(ElcidLabTest, AbstractBase):
    parasitaemia = lmodels.GenericInput()


class BabesiaFilm(Parasitaemia):
    _title = "Babesia Film"


class MalariaFilm(Parasitaemia):
    _title = "Malaria Film"


class MicrofilarialFilm(Parasitaemia):
    _title = "Microfilarial Film"


class TrypanosomesFilm(Parasitaemia):
    _title = "Trypanosomes Film"


class EBVSerology(ElcidLabTest):
    _title = "EBV Serology"
    _synonyms = "Epstein Barr Serology"

    vca_igm = lmodels.PosNegEquivicalNotDone(verbose_name="IgM")
    vca_igm = lmodels.PosNegEquivicalNotDone(verbose_name="IgG")
    ebnah_igg = lmodels.PosNegEquivicalNotDone(verbose_name="EBNA IgG")


class ViralLoad(ElcidLabTest, AbstractBase):
    viral_load = lmodels.GenericInput()


class CMVViralLoad(ViralLoad):
    _title = "CMV Viral Load"


class EBVViralLoad(ViralLoad):
    _title = "EBV Viral Load"


class HBVViralLoad(ViralLoad):
    _title = "HBV Viral Load"


class HCVViralLoad(ViralLoad):
    _title = "HCV Viral Load"


class HHV6ViralLoad(ViralLoad):
    _title = "HHV-6 Viral Load"


class HHV7ViralLoad(ViralLoad):
    _title = "HHV-7 Viral Load"


class HHV8ViralLoad(ViralLoad):
    _title = "HHV-8 Viral Load"


class HIVViralLoad(ViralLoad):
    _title = "HIV Viral Load"


class MeaslesViralLoad(ViralLoad):
    _title = "Measles PCR"


class VZVViralLoad(ViralLoad):
    _title = "VZV Viral Load"


class BKPCRViralLoad(ViralLoad):
    _title = "BK quantification"
    _synonyms = ["BK PCR"]


class CSFPCR(ElcidLabTest):
    _title = "CSF PCR"
    hsv1 = lmodels.PendingPosNeg(verbose_name="HSV 1")
    hsv2 = lmodels.PendingPosNeg(verbose_name="HSV 2")
    enterovirus = lmodels.PendingPosNeg(verbose_name="Enterovirus")
    cmv = lmodels.PendingPosNeg(verbose_name="CMV")
    ebv = lmodels.PendingPosNeg(verbose_name="EBV")
    vzv = lmodels.PendingPosNeg(verbose_name="VZV")


class HBVSerology(ElcidLabTest):
    _title = "HBV Serology"
    _synonyms = [
        "Hepatitis B serology",
        "Hep B serology",
        "Hepatitis B Serology",
    ]
    hbsag = lmodels.PosNegEquivicalNotDone(
        verbose_name="HBsAg"
    )
    antihbs = lmodels.PosNegEquivicalNotDone(
        verbose_name="anti-HbS"
    )
    antihbcoreigm = lmodels.PosNegEquivicalNotDone(
        verbose_name="anti-HbCore IgM"
    )
    antihbcoreigg = lmodels.PosNegEquivicalNotDone(
        verbose_name="anti-HbCore IgG"
    )


class HIVSerologyObservation(lmodels.Observation):
    class Meta:
        proxy = True
        auto_created = True

    RESULT_CHOICES = (
        ("antibody positive", "antibody +ve"),
        ("ap24 antigen only", "p24 antigen only"),
        ("pending", "pending"),
        ("negative", "-ve")
    )


class HIVSerology(ElcidLabTest):
    _title = "HIV Serology"
    result = HIVSerologyObservation()


class AbstractLeishmaniasisPCR(ElcidLabTest, AbstractBase):

    species = lmodels.GenericInput()
    result = lmodels.PendingPosNeg()


class LeishmaniasisPCR(ElcidLabTest):
    _title = "Leishmaniasis PCR"


class MalariaPCR(ElcidLabTest):
    _title = "Malaria PCR"


class AbstractMCS(ElcidLabTest):

    microscopy = lmodels.GenericInput()
    organism = lmodels.Organism()

    # show the sensitive antimicrobial field
    POTENTIALLY_SENSITIVE = True

    # show the resistent antimicrobial field
    POTENTIALLY_RESISTANT = True


class BALMCANDSTest(AbstractMCS):
    _title = "BAL MC&S"
    _synonyms = ["Broncheoalveolar lavage MC&S"]


class CSFMCANDSTest(AbstractMCS):
    _title = "CSF MC&S"


class FluidMCAndSTest(AbstractMCS):
    _title = "Fluid MC&S"


class LymphNodeMCAndS(AbstractMCS):
    _title = "Lymph Node MC&S"


class SputumMCAndS(AbstractMCS):
    _title = "Sputum MC&S"


class StoolMCAndS(AbstractMCS):
    _title = "Stool MC&S"


class StoolOCP(AbstractMCS):
    _title = "Stool OCP"


class ThroatSwabMCandS(AbstractMCS):
    _title = "Throat Swab MC&S"


class TissueMCandS(AbstractMCS):
    _title = "Tissue MC&S"


class UrineMCandS(AbstractMCS):
    _title = "Urine MC&S"


class WoundSwabMCandS(AbstractMCS):
    _title = "Wound swab MC&S"


class AsciticFluidMCandS(AbstractMCS):
    _title = "Ascitic Fluid MC&S"


class PleuralFluidMCandS(AbstractMCS):
    _title = "Pleural Fluid MC&S"


class PleuralBiopsyMCandS(AbstractMCS):
    _title = "Pleural Biopsy MC&S"


class UrineOCP(AbstractMCS):
    _title = "Urine OCP"


class SurgicalSiteMCandS(AbstractMCS):
    _title = "Surgical Site MC&S"


class FluidAFBMCandS(AbstractMCS):
    _title = "Fluid AFB MC&S"
    _synonyms = [
        "Fluid AFB microscopy & TB culture",
        "Fluid TB MC&S"
    ]


class CSFAFBMCandS(AbstractMCS):
    _title = "CSF AFB MC&S"
    _synonyms = [
        "CSF AFB microscopy & TB culture",
        "CSF TB MC&S"
    ]


class TissueAFBMCandS(AbstractMCS):
    _title = "Tissue AFB MC&S"
    _synonyms = [
        "Tissue AFB microscopy & TB culture",
        "Tissue TB MC&S"
    ]


class UrineAFBMCandS(AbstractMCS):
    _title = "Urine AFB MC&S"
    _synonyms = [
        "Urine AFB microscopy & TB culture",
        "Urine TB MC&S"
    ]


class SputumAFBMCandS(AbstractMCS):
    _title = "Sputum AFB MC&S"
    _synonyms = [
        "Sputum AFB microscopy & TB culture",
        "Sputum TB MC&S"
    ]


class MSU(AbstractMCS):
    _title = "MSU"
    _synonyms = [
        "Mid stream urine"
    ]


class CSU(AbstractMCS):
    _title = "CSU"
    _synonyms = [
        "Catheter specimen urine"
    ]


class BloodCulture(AbstractMCS):
    _title = "Blood Culture"
    _synonyms = [
        "BC"
    ]


class OtherAbstractTest(ElcidLabTest, AbstractBase):

    result = lmodels.GenericInput()


class Other(OtherAbstractTest):
    _title = "Other"
    _synonyms = []


class ChestXRay(OtherAbstractTest):
    _title = "Chest X-Ray"
    _synonyms = [u'CXR']


class AbdominalXRay(OtherAbstractTest):
    _title = "Abdominal X-Ray"
    _synonyms = [u'AXR']


class CT(OtherAbstractTest):
    _title = "CT"
    _synonyms = []


class US(OtherAbstractTest):
    _title = "US"
    _synonyms = []


class MRI(OtherAbstractTest):
    _title = "MRI"
    _synonyms = [u'Magnetic Resonance Imaging']


class CRP(OtherAbstractTest):
    _title = "CRP"
    _synonyms = [u'C-reactive protein']


class SixteenSPCR(OtherAbstractTest):
    _title = "16S PCR"
    _synonyms = [u'16S sequencing']


class EighteenSPCR(OtherAbstractTest):
    _title = "18S PCR"
    _synonyms = [u'18S sequencing']


class CD4(OtherAbstractTest):
    _title = "CD4"
    _synonyms = [u'CD4 count']


class TOE(OtherAbstractTest):
    _title = "TOE"
    _synonyms = [u'Transoesophageal echo']


class TTE(OtherAbstractTest):
    _title = "TTE"
    _synonyms = [u'Transthoracic echo']


class FBC(OtherAbstractTest):
    _title = "FBC"
    _synonyms = [u'Full Blood Count']


class Urinalysis(OtherAbstractTest):
    _title = "Urinalysis"
    _synonyms = []


class ParasiteID(OtherAbstractTest):
    _title = "Parasite ID"
    _synonyms = []


class Mycology(OtherAbstractTest):
    _title = "Mycology"
    _synonyms = []


class AbstractSerologyTest(ElcidLabTest, AbstractBase):

    igm = lmodels.PosNegEquivicalNotDone(verbose_name="IgM")
    igg = lmodels.PosNegEquivicalNotDone(verbose_name="IgG")


class CMVSerology(AbstractSerologyTest):
    _title = "CMV Serology"
    _synonyms = []


class DengueSerology(AbstractSerologyTest):
    _title = "Dengue Serology"
    _synonyms = []


class HepASerology(AbstractSerologyTest):
    _title = "Hep A Serology"
    _synonyms = [u'Hepatitis A Serology']


class HepESerology(AbstractSerologyTest):
    _title = "Hep E Serology"
    _synonyms = [u'Hepatitis E Serology']


class MeaslesSerology(AbstractSerologyTest):
    _title = "Measles Serology"
    _synonyms = []


class RubellaSerology(AbstractSerologyTest):
    _title = "Rubella Serology"
    _synonyms = []


class ToxoplasmosisSerology(AbstractSerologyTest):
    _title = "Toxoplasmosis Serology"
    _synonyms = []


class VZVSerology(AbstractSerologyTest):
    _title = "VZV Serology"
    _synonyms = []


class BrucellaSerology(AbstractSerologyTest):
    _title = "Brucella Serology"
    _synonyms = []


class Lymescreeningserology(AbstractSerologyTest):
    _title = "Lyme screening serology"
    _synonyms = [u'Borrelia screening serology']


class Lymereferencelabserology(AbstractSerologyTest):
    _title = "Lyme reference lab serology"
    _synonyms = [u'Borrelia reference lab serology']


class Mumps(AbstractSerologyTest):
    _title = "Mumps"
    _synonyms = []


class parvovirus(AbstractSerologyTest):
    _title = "parvovirus"
    _synonyms = [u'parvo']


class Chikungunya(AbstractSerologyTest):
    _title = "Chikungunya"
    _synonyms = []


class AbstractSinglePosNeg(ElcidLabTest, AbstractBase):

    result = lmodels.PendingPosNeg()


class CRAG(AbstractSinglePosNeg):
    _title = "CRAG"
    _synonyms = [u'Cryptococcal antigen']


class DenguePCR(AbstractSinglePosNeg):
    _title = "Dengue PCR"
    _synonyms = []


class JCVirusPCR(AbstractSinglePosNeg):
    _title = "JC Virus PCR"
    _synonyms = []


class RickettsiaPCR(AbstractSinglePosNeg):
    _title = "Rickettsia PCR"
    _synonyms = []


class ScrubTyphusPCR(AbstractSinglePosNeg):
    _title = "Scrub Typhus PCR"
    _synonyms = []


class VHFPCR(AbstractSinglePosNeg):
    _title = "VHF PCR"
    _synonyms = [u'Viral Haemorrhagic Fever PCR']


class SkinSnip(AbstractSinglePosNeg):
    _title = "Skin Snip"
    _synonyms = []


class Legionellaserology(AbstractSinglePosNeg):
    _title = "Legionella serology"
    _synonyms = []


class BKvirusqualitativePCR(AbstractSinglePosNeg):
    _title = "BK virus qualitative PCR"
    _synonyms = [u'BK PCR', u'BK virus PCR']


class ToxoplasmaPCR(AbstractSinglePosNeg):
    _title = "Toxoplasma PCR"
    _synonyms = [u'Toxo PCR']


class Pneumococcalag(AbstractSinglePosNeg):
    _title = "Pneumococcal ag"
    _synonyms = [u'Pneumococcal antigen', u'Urine pneumococcal antigen']


class Legionellaag(AbstractSinglePosNeg):
    _title = "Legionella ag"
    _synonyms = [u'Legionella antigen', u'Urine legionella antigen']


class MRSAPCR(AbstractSinglePosNeg):
    _title = "MRSA PCR"
    _synonyms = [u'MRAP']


class StoolPCR(ElcidLabTest):
    _title = "Stool PCR"

    norovirus = lmodels.PendingPosNeg()
    rotavirus = lmodels.PendingPosNeg()
    adenovirus = lmodels.PendingPosNeg()


class SwabPCR(ElcidLabTest):
    _title = "Swab PCR"

    hsv = lmodels.PendingPosNeg(verbose_name="HSV")
    vsv = lmodels.PendingPosNeg()
    syphilis = lmodels.PendingPosNeg()


class SyphilisSerology(ElcidLabTest):
    _title = "Syphilis Serology"

    rpr = lmodels.GenericInput(verbose_name="RPR")
    tppa = lmodels.PendingPosNeg(verbose_name="TPPA")
