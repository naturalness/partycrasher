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
  $httpParamSerializer,
  DEFAULT_THRESHOLD,
  PROJECT_NAMES
) {
  var threshold = $routeParams.threshold || DEFAULT_THRESHOLD,
    project = $routeParams.project || '*';

  /* Initially, we're loading. */
  $scope.loading = true;

  $scope.search = search;
  $scope.search.date = moment().subtract(3, 'days').toDate();
  $scope.search.project = project;
  $scope.search.threshold = threshold;

  $scope.projects = PROJECT_NAMES;

  /* Do the initial search. */
  search();

  /* TODO: add generic query. */
  function search() {
    $scope.loading = true;

    $http.get(searchUrl({
      project: $scope.search.project,
      threshold,
      since: $scope.search.date
    }))
      .then(({data}) => {
        $scope.results = data;
        $scope.hasResults = data['top_buckets'].length > 0;
        $scope.loading = false;

        setNewLocation();
      });
  }

  /**
   * Sets the location from the search variables.
   */
  function setNewLocation() {
    var project = $scope.search.project;
    var threshold = $scope.search.threshold;

    /* TODO: add "since" support. */
    $location.url(`/${project}/buckets/${threshold}`);
  }

  function searchUrl({project, threshold, since}) {
    var query = $httpParamSerializer({ since: since || '3-days-ago' });
    return `/${project}/buckets/${threshold}?${query}`;
  }
});
