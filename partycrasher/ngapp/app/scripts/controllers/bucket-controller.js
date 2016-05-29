'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:TopbucketsCtrl
 * @description
 * # TopbucketsCtrl
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
.controller('BucketController', function ($scope, $http, $routeParams, Bucket) {
  var project = $routeParams.project,
    threshold = $routeParams.threshold,
    id = $routeParams.id;

  $scope.loading = true;

  /* Fetch the bucket. */
  $http.get(bucketURL({ project, threshold, id }))
    .then(({data}) => {
      $scope.loading = false;
      setBucket(data);
    });

  /* TODO: What if we get an invalid bucket? */

  /**
   * TODO: Make this a server/provider thing...
   */
  function bucketURL({ project, threshold, id }) {
    return `/${project}/buckets/${threshold}/${id}`;
  }

  function setBucket(data) {
    var bucket = $scope.bucket = new Bucket(data);

    $scope.sampleReports = bucket.reports.slice(-3).map(report => {
      /* Return a subset of the fields. */
      return {
        id: report.id,
        project: report.project,
        href: report.href,
        stackTrace: report.stackTrace };
    });

    /* TODO: make this easier to use later. */
    $scope.versions = nullIfEmpty(bucket.versions);
    $scope.oses = nullIfEmpty(bucket.oses);
    $scope.builds = nullIfEmpty(bucket.build);
  }

  function nullIfEmpty(thing) {
    if (!thing) {
      return null;
    }
    return thing.length ? thing : null;
  }
});
