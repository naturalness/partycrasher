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
    from = $location.search().from,
    size = $location.search().size,
    date;

  if (since) {
    date = since;
  } else {
    date = '3-days-ago';
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
  $scope.search.project = project;
  $scope.search.from = from | 0;
  $scope.search.size = size | 0;
  $scope.search.threshold = threshold;

  $scope.projects = PROJECT_NAMES;

  /* Do the initial search. */
  search();

  function search() {
    var project = $scope.search.project,
      since = $scope.search.date,
      from = $scope.search.from,
      size = $scope.search.size,
      threshold = $scope.search.threshold;

    /* If we're searching, we're loadin' */
    $scope.loading = true;

    PartyCrasher.search({ project, threshold, since, from, size })
      .then(results => {
        $scope.hasResults = results['top_buckets'].length > 0;
        $scope.results = results;
        $scope.loading = false;
        $scope.errorMessage = null;
        setNewLocation(since, from, size);

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
        setNewLocation(since, from, size);
      });
  }

  function prevPage() {
    $scope.search.from = ($scope.search.from | 0) - ($scope.search.size | 0);
    search();
  }
  function nextPage() {
    $scope.search.from = ($scope.search.from | 0) + ($scope.search.size | 0);
    search();
  }

  /**
   * Sets the location from the search variables.
   */
  function setNewLocation(date, from, size) {
    var project = $scope.search.project;
    var threshold = $scope.search.threshold;

    $location
      .search('since', date)
      .search('from', from)
      .search('size', size)
      .path(`/${project}/buckets/${threshold}`);
  }
});
