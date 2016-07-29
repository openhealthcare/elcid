describe('Line', function(){
    "use strict";

    var Line;

    beforeEach(function(){
        module('opal.services')
        module('opal.records');
        inject(function($injector){
            Line = $injector.get('Line');
        });

    });

    describe('Initialization', function(){

        it('should set the date', function(){
            var today = moment();
            var diagnosis = new Line({});
            jasmine.clock().mockDate(today.toDate());
            expect(diagnosis.insertion_date).toEqual(today);
        });

        it('should leave the date alone if we set it already', function(){
            var diagnosis = new Line({insertion_date:'foo'});
            expect(diagnosis.insertion_date).toEqual('foo');
        })

    })

});
