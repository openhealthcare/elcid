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
            var today = moment().format('DD/MM/YY');
            var investigation = new Investigation({});
            expect(investigation.date_ordered.format('DD/MM/YY')).toEqual(today);
        });

        it('should leave the date alone if we set it already', function(){
            var note = new Investigation({date_ordered:'foo'});
            expect(note.date_ordered).toEqual('foo');
        })

    })

});
