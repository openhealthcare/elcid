angular.module('opal.controllers').controller(
    'ClinicalAdviceForm',
    function(
        $rootScope, $scope, $window,
            recordLoader, ngProgressLite,
            $cookies, Referencedata
            ){
        "use strict";

        var REASON_FOR_INTERACTION_COOKIE = "patientNotes-reasonForInteraction";
        var DISCUSSED_WITH_COOKIE = "patientNotes-discussedWith";

        /*
        * expects an episode to exist on the scope
        */
        function getCopy(item){
            var copy = item.makeCopy();
            var defaults = {
                reason_for_interaction: $cookies.get(REASON_FOR_INTERACTION_COOKIE),
                discussed_with: $cookies.get(DISCUSSED_WITH_COOKIE)
            };

            return _.extend(copy, defaults);
        }

        var self = this;

        Referencedata.then(function(referencedata){
          _.extend(self, referencedata.toLookuplists());
        });

        recordLoader.then(function(){
            var item = $scope.episode.newItem("microbiology_input", {column: $rootScope.fields.microbiology_input});
            self.editing = getCopy(item);

            self.save = function(){
              ngProgressLite.set(0);
              ngProgressLite.start();
              $cookies.put(REASON_FOR_INTERACTION_COOKIE, self.editing.reason_for_interaction || "");
              $cookies.put(DISCUSSED_WITH_COOKIE, self.editing.discussed_with || "");
              item.save(self.editing).then(function() {
                  ngProgressLite.done();
                  item = $scope.episode.newItem('microbiology_input', {column: $rootScope.fields.microbiology_input});
                  self.editing = getCopy(item);
              });
            };
        });
    }
 );
