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
            var today = moment().format('DD/MM/YY');
            var line = new Line({});
            expect(line.insertion_date.format('DD/MM/YY')).toEqual(today);
        });

        it('should leave the date alone if we set it already', function(){
            var diagnosis = new Line({insertion_date:'foo'});
            expect(diagnosis.insertion_date).toEqual('foo');
        })

    })

});
