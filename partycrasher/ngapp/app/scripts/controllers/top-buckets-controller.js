'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:TopbucketsCtrl
 * @description
 * # TopbucketsCtrl
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
.controller('TopBucketsController', function (
  $scope,
  $http,
  $routeParams,
  $httpParamSerializer,
  DEFAULT_THRESHOLD,
  PROJECT_NAMES
) {
  var threshold = $routeParams.threshold || DEFAULT_THRESHOLD,
    project = $routeParams.project || '*';

  /* Initially, we're loading. */
  $scope.loading = true;
  $scope.searchDate = moment().subtract(3, 'days').toDate();
  $scope.searchProject = project;
  $scope.search = search;

  $scope.projects = PROJECT_NAMES;

  /* Do the initial search. */
  search();

  function search() {
    $scope.loading = true;

    $http.get(searchUrl({
      project: $scope.searchProject,
      threshold,
      since: $scope.searchDate
    }))
      .then(({data}) => {
        $scope.results = data;
        $scope.hasResults = data['top_buckets'].length > 0;
        $scope.loading = false;
      });
  }

  function searchUrl({project, threshold, since}) {
    var query = $httpParamSerializer({ since: since || '3-days-ago' });
    return `/${project}/buckets/${threshold}?${query}`;
  }
});
