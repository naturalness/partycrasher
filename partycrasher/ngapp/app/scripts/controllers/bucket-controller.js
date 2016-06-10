'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:TopbucketsCtrl
 * @description
 * # TopbucketsCtrl
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
.controller('BucketController', function (
  $scope,
  $http,
  $routeParams,
  Bucket,
  PartyCrasher,
  $location
) {
  var project = $routeParams.project,
    threshold = $routeParams.threshold,
    id = $routeParams.id,
    from = $location.search().from,
    size = $location.search().size;

  $scope.loading = true;

  if (!from) {
    from = 0;
  }

  if (!size) {
    size = 10;
  }

  /* Coerce each attribute to an int. */
  $scope.from = from | 0;
  $scope.size = size | 0;
  /* TODO: handle the inevitble NaN if `from` or `size` ends up being some
   * unparasble string. */

  $scope.prevPage = prevPage;
  $scope.nextPage = nextPage;

  fetchBucket();

  function fetchBucket() {
    /* Fetch the bucket. */
    PartyCrasher.fetchBucket({ project, threshold, id,
                               from: $scope.from,
                               size: $scope.size })
      .then(bucket => {
        $scope.loading = false;
        setBucket(bucket);
      });
    /* TODO: What if we get an invalid bucket? */
  }

  function setBucket(data) {
    var bucket = $scope.bucket = new Bucket(data);

    $scope.sampleReports = bucket.reports.slice(-3).map(report => {
      /* Return a subset of the fields. */
      var thisReport = {
        id: report.id,
        project: report.project,
        href: report.href,
        stackTrace: report.stackTrace
      };
      PartyCrasher.fetchSummary({ project, id })
        .then(summary => {
          thisReport.summary = summary;
        });
      return thisReport;
    });
  }

  function prevPage() {
    var from = ($scope.from | 0) - ($scope.size | 0);
    setNewLocation(from, $scope.size);
  }

  function nextPage() {
    var from = ($scope.from | 0) + ($scope.size | 0);
    setNewLocation(from, $scope.size);
  }

  function setNewLocation(from, size) {
    var project = $routeParams.project,
      threshold = $routeParams.threshold,
      id = $routeParams.id;

    $location
      .search('from', from)
      .search('size', size)
      .path(`/${project}/buckets/${threshold}/${id}`);
  }
});
