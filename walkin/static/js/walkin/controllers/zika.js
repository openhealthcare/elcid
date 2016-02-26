//
// This controller provides a custom interface for managing Zika patients
//
controllers.controller(
    'ZikaCtrl',
    function( $scope, $modalInstance, $q, episode ){
        "use strict";

        $scope.episode = episode;
        $scope.test_names = {
            blood_zika_pcr : 'Blood ZIKA PCR',
            urine_pcr      : 'Urine ZIKA PCR',
            dengue_serology: 'Dengue serology',
            dengue_pcr     : 'Dengue PCR',
            chik_serology  : 'Chikungunya serology',
            chik_pcr       : 'Chikungunya PCR',
            dengue_chik    : 'Dengue and Chikungunya serology and PCR'
        }
        $scope.test_properties = _.invert( $scope.test_names );

        $scope.editing = {
            tests: {
                blood_zika_pcr: false,
                urine_pcr: false,
                dengue_chik: false
            },
            zika: {}
        };

        if($scope.episode.zika_pathway && $scope.episode.zika_pathway.length > 0){
            $scope.editing.zika = $scope.episode.zika_pathway[0].makeCopy();
        }

        _.each( episode.microbiology_test, function(test){
            if( test.test in $scope.test_properties ){
                $scope.editing.tests[$scope.test_properties[test.test]] = true;
            }
        });
        $scope.initial = angular.copy( $scope.editing.tests );

        $scope.save = function(){

            var saves = []

            if($scope.episode.zika_pathway && $scope.episode.zika_pathway.length > 0){
                saves.push($scope.episode.zika_pathway[0].save($scope.editing.zika));
            }else{
                var zika = $scope.episode.newItem('zika_pathway');
                saves.push(zika.save($scope.editing.zika));
            }

            _.each( _.keys( $scope.editing.tests ), function( key ){
                if( $scope.editing.tests[key] == true && !$scope.initial[key] ){
                    var test = $scope.episode.newItem( 'microbiology_test' );
                    saves.push( test.save( {
                        test: $scope.test_names[key],
                        date_ordered: moment()} ) );
                }
            });

            $scope.saving = true;
            $q.all(saves).then(
                function(){
                    $scope.saving = false;
                    $modalInstance.close();
                }
            )

        };

        // Let's have a nice way to kill the modal.
        $scope.cancel = function() {
            $scope.saving = false;
            $modalInstance.close('cancel');
        };

    }
);
