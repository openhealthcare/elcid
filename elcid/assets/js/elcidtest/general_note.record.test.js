describe('GeneralNote', function(){
    "use strict";

    var GeneralNote;

    beforeEach(function(){
        module('opal.services')
        module('opal.records');
        inject(function($injector){
            GeneralNote = $injector.get('GeneralNote');
        });

    });

    describe('Initialization', function(){

        it('should set the date', function(){
            var today = moment();
            var note = new GeneralNote({});
            jasmine.clock().mockDate(today.toDate());
            expect(note.date).toEqual(today);
        });

        it('should leave the date alone if we set it already', function(){
            var note = new GeneralNote({date:'foo'});
            expect(note.date).toEqual('foo');
        })

    })

});
