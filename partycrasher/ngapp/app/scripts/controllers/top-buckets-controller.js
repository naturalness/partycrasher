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
  PROJECT_NAMES,
  THRESHOLDS
) {
  var threshold = $routeParams.threshold || DEFAULT_THRESHOLD,
    project = $routeParams.project || '*',
    since = $location.search().since,
    date;

  if (since) {
    date = since;
  } else {
    date = "3-days-ago";
  }

  if (Number.isNaN(date.valueOf())) {
    throw new RangeError(`Could not parse date ${since}`);
  }

  /* Initially, we're loading. */
  $scope.loading = true;
  $scope.thresholds = THRESHOLDS;

  /* Note! The weird date picker thing DEMANDS that the date property be
   * wrapped an object of some kind (viz. search). */
  $scope.search = search;
  $scope.search.date = date;
  $scope.search.project = project;
  $scope.search.thresholdIndex = THRESHOLDS.indexOf(threshold);

  /*
   * Allows returning the string value of the threshold, even if only the list
   * index value of the threshold is known.
   */
  Object.defineProperty($scope.search, 'threshold', {
    get: function () {
      return THRESHOLDS[$scope.search.thresholdIndex];
    },

    set: function () {
      throw new Error(`Cannot directly set threshold.`);
    }
  });

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
        $scope.hasResults = results['top_buckets'].length > 0;
        $scope.results = results;
        $scope.loading = false;
        $scope.errorMessage = null;
        setNewLocation(since);
      }).catch(error => {
        $scope.hasResults = false;
        $scope.results = null;
        $scope.errorMessage = error.data.message;
        $scope.loading = false;
        setNewLocation(since);
      });
  }

  /**
   * Sets the location from the search variables.
   */
  function setNewLocation(date) {
    var project = $scope.search.project;
    var threshold = $scope.search.threshold;

    $location
      .search('since', date)
      .path(`/${project}/buckets/${threshold}`);
  }
});
