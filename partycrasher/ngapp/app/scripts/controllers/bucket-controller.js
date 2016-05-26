'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:TopbucketsCtrl
 * @description
 * # TopbucketsCtrl
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
.controller('BucketController', function ($scope, Bucket, SAMPLE_BUCKET, $http, $routeParams) {
  var project = $routeParams.project || '*',
    /* no default threshold, since this is a SPECIFIC bucket. */
    threshold = $routeParams.threshold,
    id = $routeParams.id;

  $scope.loading = true;

  setBucket(SAMPLE_BUCKET);

  /* Fetch the bucket. */
  $http.get(bucketURL({ project, threshold, id }))
    .then(({data}) => {
      $scope.loading = false;
      false && Object.assign($scope, data);
    });

  function bucketURL({ project, threshold, id }) {
    return `/${project}/buckets/${threshold}/${id}`;
  }

  function setBucket(data) {
    var bucket = $scope.bucket = new Bucket(data);
    /* Cool metadata. */
    $scope.versions = nullIfEmpty(bucket.versions);
    $scope.oses = nullIfEmpty(bucket.oses);
    $scope.builds = nullIfEmpty(bucket.build);
  }

  function nullIfEmpty(thing) {
    if (!thing)
      return null;
    return thing.length ? thing : null;
  }
});
