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
            var today = moment().format('DD/MM/YY');
            var note = new GeneralNote({});
            expect(note.date.format('DD/MM/YY')).toEqual(today);
        });

        it('should leave the date alone if we set it already', function(){
            var note = new GeneralNote({date:'foo'});
            expect(note.date).toEqual('foo');
        })

    })

});
