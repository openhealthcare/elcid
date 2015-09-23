angular.module('opal.controllers').controller(
    'ClinicalAdviceForm', function($rootScope, $scope, $window,
                                 recordLoader, ngProgressLite, $q,
                                 $cookieStore
                                    ){
        var REASON_FOR_INTERACTION_COOKIE = "patientNotes-reasonForInteraction";
        var DISCUSSED_WITH_COOKIE = "patientNotes-discussedWith";
        /*
        * expects an episode to exist on the scope
        */
        function getCopy(item){
            var copy = item.makeCopy();
            defaults = _.clone({
                when: new Date(),
                initials: $window.initials,
                reason_for_interaction: $cookieStore.get(REASON_FOR_INTERACTION_COOKIE),
                discussed_with: $cookieStore.get(DISCUSSED_WITH_COOKIE)
            });

            return _.extend(copy, defaults);
        }

        var self = this;
        recordLoader.then(function(){
            var item = $scope.episode.newItem("microbiology_input", {column: $rootScope.fields.microbiology_input});
            self.editing = getCopy(item);

            self.save = function(){
                    ngProgressLite.set(0);
                    ngProgressLite.start();
                    $cookieStore.put(REASON_FOR_INTERACTION_COOKIE, self.editing.reason_for_interaction || "");
                    $cookieStore.put(DISCUSSED_WITH_COOKIE, self.editing.discussed_with || "");
                    to_save = [item.save(self.editing)];
                    $q.all(to_save).then(function() {
                        ngProgressLite.done();
                        item = $scope.episode.newItem('microbiology_input', {column: $rootScope.fields.microbiology_input});
                        self.editing = getCopy(item);
                    });
            };
        });
    }
 );
