//
// This controller provides a custom interface for Walkin nurses to create many
// investigations at once.
//
controllers.controller(
    'WalkinNurseInvestigationsCtrl',
    function( $scope, $modalInstance, $q, episode ){
        "use strict";

        $scope.investigations = {};
        $scope.episode        = episode;
        $scope.saving = false;

        $scope.test_names = {
            blood_culture      : 'Blood Culture',
            urine_mcs          : 'Urine MC&S',
            wound_swab_mcs     : 'Wound swab MC&S',
            throat_swab_mcs    : 'Throat swab MC&S',
            stool_mcs          : 'Stool MC&S',
            stool_ocp          : 'Stool OCP',
            malaria_film       : 'Malaria Film',
            full_blood_count   : 'Full Blood Count',
            biochemistry       : 'Biochemistry',
            serum_save         : 'Serum Save',
            resp_pcr           : 'Respiratory Virus PCR',
            chikungunya        : 'Chikungunya',
            dengue             : 'Dengue',
            parasite_id        : 'Parasite ID',
            rickettsia_serology: 'Rickettsia Serology'
        }
        $scope.test_properties = _.invert( $scope.test_names );

        _.each( episode.microbiology_test, function(test){
            if( test.test in $scope.test_properties ){
                $scope.investigations[$scope.test_properties[test.test]] = true;
            }
        });
        $scope.initial = angular.copy( $scope.investigations );


        $scope.save = function(){
            var saves = [];
            _.each( _.keys( $scope.investigations ), function( key ){
                if( $scope.investigations[key] == true && !$scope.initial[key] ){
                    var test = $scope.episode.newItem( 'microbiology_test' );
                    saves.push( test.save( {
                        test: $scope.test_names[key],
                        date_ordered: moment()} ) );
                }
            });
            if( saves.length > 0 ){
                $scope.saving = true;
                $q.all( saves ).then(
                    function(){
                        $scope.saving = false;
                        $modalInstance.close();
                    }
                );
            }else{
                $modalInstance.close();
            }
        };

        // Let's have a nice way to kill the modal.
        $scope.cancel = function() {
            $scope.saving = false;
            $modalInstance.close('cancel');
        };

    }
);
