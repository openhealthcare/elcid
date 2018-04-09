describe('OPATLineAssessment', function(){
    "use strict";

    var OPATLineAssessment;

    beforeEach(function(){
        module('opal.services')
        module('opal.records');
        inject(function($injector){
            OPATLineAssessment = $injector.get('OPATLineAssessment');
        });

    });

    describe('Initialization', function(){

        it('should set the date', function(){
            var today = moment().format('DD/MM/YY');
            var opatLineAssessment = new OPATLineAssessment({});
            expect(opatLineAssessment.assessment_date.format('DD/MM/YY')).toEqual(today)
        });

        it('should leave the date alone if we set it already', function(){
            var ass = new OPATLineAssessment({assessment_date:'foo'});
            expect(ass.assessment_date).toEqual('foo');
        })

    })

});
