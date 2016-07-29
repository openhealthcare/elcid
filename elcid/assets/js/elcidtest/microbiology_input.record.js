describe('MicrobiologyInput', function(){
    "use strict";

    var $window;
    var MicrobiologyInput;

    beforeEach(function(){
        module('opal.services')
        module('opal.records');
        inject(function($injector){
            MicrobiologyInput = $injector.get('MicrobiologyInput');
            $window          = $injector.get('$window');
        });

    });

    describe('Initialization', function(){

        it('should set the date', function(){
            var today = moment();
            var ca = new MicrobiologyInput({});
            jasmine.clock().mockDate(today.toDate());
            expect(ca.when).toEqual(today);
        });

        it('should set the initials', function(){
            $window.initials = 'S. Holmes';
            var ca = new MicrobiologyInput({});
            expect(ca.initials).toEqual('S. Holmes');
        });

        it('should leave the date alone if we set it already', function(){
            var ca = new MicrobiologyInput({when:'foo'});
            expect(ca.when).toEqual('foo');
        });

        it('should leave the initials alone if we set them already', function(){
            var ca = new MicrobiologyInput({initials:'foo'});
            expect(ca.initials).toEqual('foo');
        })

    })

});
