describe('Diagnosis', function(){
    "use strict";

    var Diagnosis;

    beforeEach(function(){
        module('opal.services')
        module('opal.records');
        inject(function($injector){
            Diagnosis = $injector.get('Diagnosis');
        });

    });

    describe('Initialization', function(){

        it('should set the date', function(){
            var today = moment();
            var diagnosis = new Diagnosis({});
            jasmine.clock().mockDate(today.toDate());
            expect(diagnosis.date_of_diagnosis).toEqual(today);
        });

        it('should leave the date alone if we set it already', function(){
            var diagnosis = new Diagnosis({date_of_diagnosis:'foo'});
            expect(diagnosis.date_of_diagnosis).toEqual('foo');
        })

    })

});
