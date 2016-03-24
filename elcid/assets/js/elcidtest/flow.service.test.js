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
            expect(Flow.exit({category: 'Walkin'})).toEqual(walkin_exit);
        });

    });

    describe('Inpatients', function() {

        it('enter should fetch the default flow', function() {
            expect(Flow.enter()).toEqual(inpatient_default_enter);
        });

        it('should fetch hte default exit flow', function() {
            expect(Flow.exit({category: 'Inpatient'})).toEqual(inpatient_default_exit);
        });
    });

});
