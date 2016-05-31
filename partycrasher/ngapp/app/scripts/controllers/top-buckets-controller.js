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
    from = $location.search().from,
    size = $location.search().size,
    date;

  if (since) {
    date = since;
  } else {
    date = "3-days-ago";
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
  $scope.thresholds = THRESHOLDS;

  /* Note! The weird date picker thing DEMANDS that the date property be
   * wrapped an object of some kind (viz. search). */
  $scope.search = search;
  $scope.search.date = date;
  $scope.search.project = project;
  $scope.search.from = from;
  $scope.search.size = size;
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
      from = $scope.search.from,
      size = $scope.search.size,
      threshold = $scope.search.threshold;
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
          PartyCrasher.fetchBucket({ project, threshold, id })
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
  
  $scope.prevPage = prevPage;
  $scope.nextPage = nextPage;

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
