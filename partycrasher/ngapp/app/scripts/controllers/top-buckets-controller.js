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
  $location,
  DEFAULT_THRESHOLD,
  PartyCrasher,
  PROJECT_NAMES
) {
  var threshold = $routeParams.threshold || DEFAULT_THRESHOLD,
    project = $routeParams.project || '*',
    since = $location.search().since;

  if (since) {
    since = new Date(since);
  } else {
    since = moment().subtract(3, 'days').toDate();
  }

  /* Initially, we're loading. */
  $scope.loading = true;

  $scope.search = search;
  $scope.search.date = since;
  $scope.search.project = project;
  $scope.search.threshold = threshold;

  $scope.projects = PROJECT_NAMES;

  /* Do the initial search. */
  search();

  /* TODO: add generic query. */
  function search() {
    var project = $scope.search.project,
      since = $scope.search.date,
      threshold = $scope.search.threshold;

    $scope.loading = true;

    PartyCrasher.search({ project, threshold, since})
      .then(results => {
        $scope.results = results;
        $scope.hasResults = results['top_buckets'].length > 0;
        $scope.loading = false;
        /* TODO: do something with data['since']. */

        setNewLocation();
      });
  }

  /**
   * Sets the location from the search variables.
   */
  function setNewLocation() {
    var project = $scope.search.project;
    var threshold = $scope.search.threshold;
    var since = $scope.search.date.toISOString();

    $location
      .search('since', since)
      .path(`/${project}/buckets/${threshold}`);
  }
});
