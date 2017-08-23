// 
// Discharge Flow controller for research studies.
//
controllers.controller(
    'ResearchStudyDischargeCtrl',
    function(
        $scope, $modalInstance,
        episode, tags
    ){
        // Setup initial vars
        $scope.tags    = tags;
        $scope.episode = episode;

        var admission;
        if(episode.start){
            admission = moment(episode.start).format('MM/DD/YY')
        }

        $scope.editing = {
            start: admission,
	    category: 'ineligible',
            end: null
        };

        
        // 
        // Discharging an episode requires updating three server-side entities:
        //
        // * Location
        // * Tagging
        // * Episode
        // 
        // Make these requests then kill our modal.
        // 
        $scope.discharge = function(){
	    var tagging = episode.getItem('tagging', 0);
            var location = episode.getItem('location', 0);
            
	    var taggingAttrs = tagging.makeCopy();
            var locationAttrs = location.makeCopy();
            var episodeAttrs = episode.makeCopy();

	    locationAttrs.category = $scope.editing.category;
            episodeAttrs.end = $scope.editing.end;

            // 
            // Set tagging attributes to what they need to be
            // 
	    taggingAttrs[$scope.tags.tag] = false;
	    taggingAttrs[$scope.tags.tag+'_scientist'] = false;
	    taggingAttrs[$scope.tags.tag+'_research_practitioner'] = false;

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
