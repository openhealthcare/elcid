//
// This is the eLCID custom implementation of a discharge episode controller.
// It is included from the eLCID extra aplication template as defined in
// settings.py
//
controllers.controller('DischargeEpisodeCtrl', function($scope, $timeout,
                                                        $modalInstance, episode,
                                                        currentTag, currentSubTag) {
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
	category: newCategory
    };

    $scope.episode = episode.makeCopy();
    if(!$scope.episode.discharge_date){
        $scope.episode.discharge_date = moment().format('DD/MM/YYYY');
    }

    $scope.discharge = function() {
	var tagging = episode.getItem('tagging', 0);
	var attrs = tagging.makeCopy();

	if ($scope.editing.category != 'Unfollow') {
	    attrs.category = $scope.editing.category;
	}

        if($scope.editing.category == 'Unfollow') {
            // No longer under active review does not set a discharge date
            $scope.episode.discharge_date = null;
        }

	if ($scope.editing.category != 'Followup') {
	    attrs[currentTag] = false;
            if(currentSubTag != 'all'){
                attrs[currentSubTag] = false;
            }
	}

	tagging.save(attrs).then(function() {
	    $modalInstance.close('discharged');
	});
    };

    $scope.cancel = function() {
	$modalInstance.close('cancel');
    };
});
