//
// This is the eLCID custom implementation of a discharge episode controller.
// It is included from the eLCID extra aplication template as defined in
// settings.py
//
// TODO: Refactor the inclusion to be via a plugin.
// TODO: Set the controller more explicitly via flow
//
controllers.controller(
    'ElcidDischargeEpisodeCtrl', 
    function($scope, $timeout,
             $modalInstance, episode,
             tags) {

        var currentTag = tags.tag;
        var currentSubTag = tags.subtag;
        // TODO: Reimplement this.
        //
        // $timeout(function() {
        //     dialog.modalEl.find('input,textarea').first().focus();
        // });

        $scope.currentCategory = episode.location[0].category;
        var newCategory;

        if ($scope.currentCategory == 'Inpatient') {
	    newCategory = 'Discharged';
        } else if ($scope.currentCategory == 'Review' ||
                   $scope.currentCategory == 'Followup') {
	    newCategory = 'Unfollow';
        } else {
	    newCategory = $scope.currentCategory;
        }

        $scope.editing = {
            date_of_admission: moment(episode.date_of_admission).format('MM/DD/YY'),
	    category: newCategory,
            discharge_date: null
        };

        $scope.episode = episode.makeCopy();
        if(!$scope.episode.discharge_date){
            $scope.editing.discharge_date = moment().format('DD/MM/YYYY');
        }else{
            $scope.editing.discharge_date = $scope.episode.discharge_date;
        }

        // 
        // Discharging an episode requires updating three server-side entities:
        //
        // * Location
        // * Tagging
        // * Episode
        // 
        // Make these requests then kill our modal.
        // 
        $scope.discharge = function() {

	    var tagging = episode.getItem('tagging', 0);
            var location = episode.getItem('location', 0);
            
	    var taggingAttrs = tagging.makeCopy();
            var locationAttrs = location.makeCopy();
            var episodeAttrs = episode.makeCopy();

	    if ($scope.editing.category != 'Unfollow') {
	        locationAttrs.category = $scope.editing.category;
	    }

            if($scope.editing.category == 'Unfollow') {
                // No longer under active review does not set a discharge date
                episodeAttrs.discharge_date = null;
            }else{
                episodeAttrs.discharge_date = $scope.editing.discharge_date;
            }

	    if ($scope.editing.category != 'Followup') {
	        taggingAttrs[currentTag] = false;
                if(currentSubTag != 'all'){
                    taggingAttrs[currentSubTag] = false;
                }
	    }

	    tagging.save(taggingAttrs).then(function(){
                location.save(locationAttrs).then(function(){
                    episode.save(episodeAttrs).then(function(){
                        $modalInstance.close('discharged');            
                    })
                })

	    });
        };

        $scope.cancel = function() {
	    $modalInstance.close('cancel');
        };
    });
