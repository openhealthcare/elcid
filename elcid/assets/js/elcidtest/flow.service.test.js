describe('elCIDFlow', function() {
    "use strict";
    var $routeParams;
    var Flow;

    var walkin_enter = {
        'controller': 'WalkinHospitalNumberCtrl',
        'template'  : '/templates/modals/hospital_number.html/'
    };
    var walkin_exit =  {
        'controller': 'WalkinDischargeCtrl',
        'template'  : '/templates/modals/discharge_walkin_episode.html/'
    };
    var inpatient_default_enter = {
        'controller': 'HospitalNumberCtrl',
        'template'  : '/templates/modals/hospital_number.html/'
    };
    var inpatient_default_exit =  {
        'controller': 'ElcidDischargeEpisodeCtrl',
        'template'  : '/templates/modals/discharge_episode.html/'
    };
    var diagnosis_enter = {
        'controller': 'DiagnosisHospitalNumberCtrl',
        'template'  : '/templates/modals/hospital_number.html/'
    };
    var diagnosis_exit = {
        'controller': 'DiagnosisDischargeCtrl',
        'template'  : '/templates/elcid/modals/diagnosis_discharge.html'
    };
    var virology_enter = {
        'controller': 'VirologyHospitalNumberCtrl',
        'template'  : '/templates/modals/hospital_number.html/'
    };
    var opat_enter = {
        'controller': 'OPATReferralCtrl',
        'template'  : '/opat/templates/modals/opat_referral.html/'
    };
    var opat_exit =  {
        'controller': 'OPATDischargeCtrl',
        'template'  : '/opat/templates/modals/discharge_opat_episode.html/'
    };

    beforeEach(function(){
        module('opal.services');
        inject(function($injector){
            $routeParams = $injector.get('$routeParams');
            Flow         = $injector.get('elCIDFlow');
        });

    });

    describe('Walkin', function() {

        beforeEach(function(){
            $routeParams.slug = 'walkin-walkin_doctor';
        });

        it('should enter should fetch the flow', function() {
            expect(Flow.enter()).toEqual(walkin_enter);
        });

        it('should fetch the exit flow', function() {
            expect(Flow.exit({category_name: 'Walkin'})).toEqual(walkin_exit);
        });

    });

    describe('Inpatients', function() {

        it('enter should fetch the default flow', function() {
            expect(Flow.enter()).toEqual(inpatient_default_enter);
        });

        it('should fetch the default exit flow', function() {
            expect(Flow.exit({category_name: 'Inpatient'})).toEqual(inpatient_default_exit);
        });

        describe('Discharge Overrides', function() {
            var slugs;

            beforeEach(function(){
                slugs = [
                    'hiv-immune_inpatients',
                    'infectious_diseases-id_inpatients',
                    'tropical_diseases'
                ];
                $routeParams.slug = 'tropical_diseases';
            });

            it('enter should fetch the diagnosis flow', function() {
                _.each(slugs, function(slug){
                    $routeParams.slug = slug;
                    expect(Flow.enter()).toEqual(diagnosis_enter);
                });
            });

            it('should fetch the diagnosis exit flow', function() {
                _.each(slugs, function(slug){
                    $routeParams.slug = slug;
                    expect(Flow.exit({category_name: 'Inpatient'})).toEqual(diagnosis_exit);
                });
            });

            it('enter should fetch the diagnosis flow', function() {
                $routeParams.slug = 'virology';
                expect(Flow.enter()).toEqual(virology_enter);
            });


        });
    });

    describe('OPAT', function() {

        beforeEach(function(){
            $routeParams.slug = 'opat-opat_current';
        });

        it('should enter should fetch the flow', function() {
            expect(Flow.enter()).toEqual(opat_enter);
        });

        it('should fetch the exit flow', function() {
            expect(Flow.exit({category_name: 'OPAT'})).toEqual(opat_exit);
        });

    });

});
