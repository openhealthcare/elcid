describe('OPATReview', function(){
    "use strict";

    var $window;
    var OPATReview;

    beforeEach(function(){
        module('opal.services')
        module('opal.records');
        inject(function($injector){
            OPATReview = $injector.get('OPATReview');
            $window    = $injector.get('$window');
        });

    });

    describe('Initialization', function(){

        it('should set the date', function(){
            var today = moment();
            var review = new OPATReview({});
            expect(review.datetime).toEqual(today);
        });

        it('should set the initials', function(){
            $window.initials = 'S. Holmes';
            var review = new OPATReview({});
            expect(review.initials).toEqual('S. Holmes');
        });

        it('should leave the date alone if we set it already', function(){
            var review = new OPATReview({datetime:'foo'});
            expect(review.datetime).toEqual('foo');
        });

        it('should leave the initials alone if we set them already', function(){
            var review = new OPATReview({initials:'foo'});
            expect(review.initials).toEqual('foo');
        })

    })

});
