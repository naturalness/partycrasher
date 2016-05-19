'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:TopbucketsCtrl
 * @description
 * # TopbucketsCtrl
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
.controller('BucketController', function ($scope, $http, $routeParams) {
  var project = $routeParams.project || '*',
    /* no default threshold, since this is a SPECIFIC bucket. */
    threshold = $routeParams.threshold,
    id = $routeParams.id;

  $scope.loading = true;
  
  $http.get(bucketURL({ project, threshold, id }))
    .then(({data}) => {
      $scope.loading = false;
      Object.assign($scope, data);
    })
    .catch((data) => {
      console.error(data);
    });

  function bucketURL({ project, threshold, id }) {
    return `/${project}/buckets/${threshold}/${id}`;
  }
});
