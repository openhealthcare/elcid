angular.module('opal.controllers').controller(
    'MicroHaemDiscussionForm', function($rootScope, $scope, $window,
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
                    defaults ={
                        when: new moment(),
                        when: new moment(),
                        initials: $window.initials,
                        reason_for_interaction: "Microbiology meeting"
                    };
                    angular.extend(self.editing, defaults);
                    to_save = [item.save(self.editing)];
                    $q.all(to_save).then(function() {
                        ngProgressLite.done();
                        item = $scope.episode.newItem('microbiology_test', {column: $rootScope.fields.microbiology_input});
                        self.editing = item.makeCopy();
                        angular.extend(self.editing, defaults);
                    });
            };
        });
    }
 );
