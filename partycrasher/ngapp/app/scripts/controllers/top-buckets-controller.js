'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:TopBucketsController
 * @description
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
.controller('TopBucketsController', function (
  $scope,
  $routeParams,
  $location,
  DEFAULT_THRESHOLD,
  PartyCrasher,
  PROJECT_NAMES
) {
  var threshold = $routeParams.threshold || DEFAULT_THRESHOLD,
    project = $routeParams.project || '*',
    since = $location.search().since,
    until = $location.search().until,
    from = $location.search().from,
    size = $location.search().size,
    date;

  if (since) {
    date = since;
  } else {
    date = '3-days-ago';
  }
  
  if (!until) {
    until = '';
  }

  if (!from) {
    from = 0;
  }

  if (!size) {
    size = 10;
  }

  if (Number.isNaN(date.valueOf())) {
    throw new RangeError(`Could not parse date ${since}`);
  }

  /* Initially, we're loading. */
  $scope.loading = true;

  /* Expose a few functions (defined below). */
  $scope.search = search;
  $scope.prevPage = prevPage;
  $scope.nextPage = nextPage;

  /* Note! The weird date picker thing DEMANDS that the date property be
   * wrapped an object of some kind (viz. search). */
  $scope.search.date = date;
  $scope.search.until = until;
  $scope.search.project = project;
  $scope.search.from = from | 0; // | 0 coerces to numeric type
  $scope.search.size = size | 0;
  $scope.search.threshold = threshold;

  $scope.projects = PROJECT_NAMES;

  /* If we're searching, we're loadin' */
  $scope.loading = true;

  /* Actually do the search: only occurs on page load */
  PartyCrasher.searchTopBuckets({ project, threshold, since, until, from, size })
    .then(results => {
      $scope.hasResults = results['top_buckets'].length > 0;
      $scope.results = results;
      $scope.loading = false;
      $scope.errorMessage = null;

      results['top_buckets'].forEach(function(thisBucket) {
        var id = thisBucket['id'];
        return PartyCrasher.fetchBucket({ project, threshold, id })
          .then(bucket => {
            var id = bucket['top_reports'][0]['database_id'];
            thisBucket.database_id = id;
            thisBucket.project = bucket['top_reports'][0]['project'];
          });
      });
    }).catch(error => {
      $scope.hasResults = false;
      $scope.results = null;
      $scope.errorMessage = error.data.message;
      $scope.loading = false;
    });

  /**
   * Sets the location from the search variables.
   * 
   * Only called when search button is pressed and then changes the location
   * which causes the controller to be re-run which does the actual search. 
   */
  function search() {
    var project = $scope.search.project,
      since = $scope.search.date,
      until = $scope.search.until,
      from = $scope.search.from,
      size = $scope.search.size,
      threshold = $scope.search.threshold;
    until = until || null;
    $location
      .search('since', since)
      .search('until', until)
      .search('from', from)
      .search('size', size)
      .path(`/${project}/buckets/${threshold}`);
  }

  function prevPage() {
    $scope.search.from = ($scope.search.from | 0) - ($scope.search.size | 0);
    search();
  }
  function nextPage() {
    $scope.search.from = ($scope.search.from | 0) + ($scope.search.size | 0);
    search();
  }

});
