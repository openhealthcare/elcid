describe('Investigation', function(){
    "use strict";

    var Investigation;

    beforeEach(function(){
        module('opal.services')
        module('opal.records');
        inject(function($injector){
            Investigation = $injector.get('Investigation');
        });

    });

    describe('Initialization', function(){

        it('should set the date', function(){
            var today = moment();
            var note = new Investigation({});
            jasmine.clock().mockDate(today.toDate());
            expect(note.date_ordered).toEqual(today);
        });

        it('should leave the date alone if we set it already', function(){
            var note = new Investigation({date_ordered:'foo'});
            expect(note.date_ordered).toEqual('foo');
        })

    })

});
