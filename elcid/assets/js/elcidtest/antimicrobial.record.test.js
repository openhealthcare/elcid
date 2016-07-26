describe('Antimicrobial', function(){
    "use strict";

    var $routeParams;
    var Antimicrobial;

    beforeEach(function(){
        module('opal.services')
        module('opal.records');
        inject(function($injector){
            Antimicrobial = $injector.get('Antimicrobial');
            $routeParams  = $injector.get('$routeParams');
        });

    });

    describe('Initialization', function(){

        it('should set the date if we are in walkin', function(){
            var today = moment();
            jasmine.clock().mockDate(today.toDate());
            $routeParams.slug = 'walkin-walkin_doctor';
            var a = new Antimicrobial({});
            expect(a.start_date).toEqual(today);
        });

        it('should leave the start date alone if we are not in walkin', function(){
            var a = new Antimicrobial({});
            expect(a.initials).toEqual(undefined);
            expect(a.start_date).toEqual(undefined);
        })

        it('should leave the start date alone if we set them already', function(){
            var a = new Antimicrobial({start_date:'foo'});
            expect(a.start_date).toEqual('foo');
        })

    })

});
