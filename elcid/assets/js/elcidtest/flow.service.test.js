describe('elCIDFlow', function() {
    "use strict";
    var $routeParams;
    var Flow;

    var inpatient_default = {
        'controller': 'HospitalNumberCtrl',
        'template'  : '/templates/modals/hospital_number.html/'
    }

    beforeEach(function(){
        module('opal.services');
        inject(function($injector){
            $routeParams = $injector.get('$routeParams');
            Flow         = $injector.get('elCIDFlow');
        });

    });

    describe('Inpatients', function() {
        describe('enter', function() {
            it('should fetch the default flow', function() {
                expect(Flow.enter()).toEqual(inpatient_default);
            });
        });
    });

});
