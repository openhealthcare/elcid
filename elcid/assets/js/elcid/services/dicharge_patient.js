angular.module('opal.services').factory('DischargePatientService', function($q) {
    var DischargePatientService = function(episode, tags){
        /* has 2 jobs
        * i) create the editing fields for the template
        * ii) return a promise dicharging those fields
        */

        this.getEditing = function(episode){
            var newCategory,
                admission,
                end,

            currentCategory = episode.location[0].category;

            if(!currentCategory.length){
                currentCategory = episode.category_name;
            }

            if (currentCategory.toUpperCase() == 'Inpatient'.toUpperCase()) {
          	    newCategory = 'Discharged';
            } else if (currentCategory == 'Review' ||
                       currentCategory == 'Followup') {
          	    newCategory = 'Unfollow';
            } else {
          	    newCategory = currentCategory;
            }

            if(episode.start){
                admission = moment(episode.start).format('MM/DD/YY')
            }

            if(!episode.end){
                end = new Date();
            }else{
                if(_.isString(episode.end)){
                    end = moment(episode.end, 'DD/MM/YYYY').toDate();
                }
                else{
                    // allows for the fact that episode.end is a moment
                    // or a date. It should always be a moment
                    end = moment(episode.end).toDate();
                }
            }

            return {
                start: admission,
          	    category_name: newCategory,
                end: end
            };
        };

        this.discharge = function(episode, editing, tags){
            var currentTag,
                currentSubTag,
                tagging = episode.getItem('tagging', 0),
                location = episode.getItem('location', 0),
                taggingAttrs = tagging.makeCopy(),
                locationAttrs = location.makeCopy(),
                episodeAttrs = episode.makeCopy();

            if(tags){
                currentTag = tags.tag;
                currentSubTag = tags.subtag;
            }else{
                currentTag = 'mine';
                currentSubTag = 'all';
            }

            if (editing.category != 'Unfollow') {
                locationAttrs.category = editing.category;
            }

            if(editing.category == 'Unfollow') {
                // No longer under active review does not set a discharge date
                episodeAttrs.end = null;
            }else{
                episodeAttrs.end = editing.end;
            }

            if (editing.category != 'Followup') {
              if(currentSubTag != ''){
                  taggingAttrs[currentSubTag] = false;
              }else{
                  taggingAttrs[currentTag] = false;
              }
            }

            var deferred = $q.defer();

            tagging.save(taggingAttrs).then(function(){
                location.save(locationAttrs).then(function(){
                    episode.save(episodeAttrs).then(function(result){
                      deferred.resolve(result);
                    });
                });
            });

            return deferred.promise;
        };
    };

    return DischargePatientService;
});
