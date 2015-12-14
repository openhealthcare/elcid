//
// Editing/detail page for ward round episodes
//
angular.module('opal.wardround.controllers').controller(
   'WardRoundDetailCtrl', function($rootScope, $scope, $routeParams, $location,
                                   $cookieStore, $modal,
                                   EpisodeDetailMixin, Flow,
                                   ward_round, options, profile){

       $scope.filters = $cookieStore.get('wardround_filters') || [];
       $scope.ward_round = ward_round;
       $scope.episodes = ward_round.episodes;
       $scope.limit = ward_round.episodes.length;
       $scope.episode_id = $routeParams.episode_id;
       $scope.episode = _.findWhere($scope.ward_round.episodes, {id: parseInt($scope.episode_id)});

       $scope.options = options;
       $scope.profile = profile;
       $scope.Flow = Flow;

       EpisodeDetailMixin($scope);

       $scope.wardRoundOrderCollapsed = true;

        //
        // Iterate over our active filters and restrict the episodes accordingly
        //
        $scope.set_visible_episodes = function(){
            var episodes = $scope.episodes;
            _.each(_.keys($scope.filters), function(filter){
                var filter_expression = $scope.ward_round.filters[filter];
                episodes = _.filter(episodes, function(episode){
                    var value = $scope.filters[filter];
                    return eval(filter_expression);
                });
            });
            $scope.results = episodes;
        };
       $scope.set_visible_episodes();
       $scope.total_episodes = $scope.results.length;
       $scope.this_episode_number = _.indexOf(_.pluck($scope.results, 'id'), parseInt($scope.episode_id));

       $scope.jumpToEpisode = function(e){
           $location.path($routeParams.wardround + '/' + e.id);
       };

       $scope.next = function(){
           $scope.jumpToEpisode($scope.results[$scope.this_episode_number + 1]);
       };

       $scope.previous = function(){
           $scope.jumpToEpisode($scope.results[$scope.this_episode_number - 1]);
       };

       $scope.named_controller = function(template, controller){
           $modal.open({
               templateUrl: template,
               controller: controller,
               resolve: {
                   episode: function(){ return $scope.episode },
                   tags: function(){ return {}  },
                   schema: function(){ return {} },
                   options: function(){ return options }
               }
           });
       }
   }
);
