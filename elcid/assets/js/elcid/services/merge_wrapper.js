angular.module('opal.services').service('MergeWrapper', function($modal){
    // when adding a new patient if the patient
    // is there already exists a patient we want to bring up the merge
    // screen and give the patient an option to click through to the merge
    // screen

    // essentially it returns a function for what to do if there's a merge
    this.openMergeModal = function(someFun, goBack){
        return function(result){
          if(result.merged && result.merged.length){
            return $modal.open( {
                templateUrl: '/templates/elcid/modals/merge_patient.html/',
                controller: 'MergePatientCtrl',
                size: 'lg',
                resolve: {
                    result: function() {
                        return result;
                    },
                    nextStage: function(){
                        return someFun;
                    },
                    goBack: function(){
                        return goBack;
                    }
                }
            })
          }
          else{
              return someFun(result);
          }
        }
    };
});
