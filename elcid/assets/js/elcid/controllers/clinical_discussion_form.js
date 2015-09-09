angular.module('opal.controllers').controller(
    'ClinicalDiscussionForm', function($rootScope, $scope, $window,
                                 recordLoader, ngProgressLite, $q
                                    ){
        /*
        * expects an episode to exist on the scope
        */
        var self = this;
        recordLoader.then(function(){
            var item = $scope.episode.newItem("microbiology_input", {column: $rootScope.fields.microbiology_input});
            self.editing = item.makeCopy();

            self.save = function(){
                    ngProgressLite.set(0);
                    ngProgressLite.start();
                    to_save = [item.save(self.editing)];
                    $q.all(to_save).then(function() {
                        ngProgressLite.done();
                        item = $scope.episode.newItem('microbiology_test', {column: $rootScope.fields.microbiology_input});
                        self.editing = item.makeCopy();
                    });
            };
        });
    }
 );
