'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:CrashController
 * @description
 * # TopbucketsCtrl
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
.controller('CrashController', function (
  $scope,
  $routeParams,
  PartyCrasher,
  CrashReport
) {
  var project = $routeParams.project,
    id = $routeParams.id;

  PartyCrasher.fetchReport({ project, id })
    .then(rawReport => {
      var report = $scope.crash = new CrashReport(rawReport);
      $scope.stack = report.stackTrace;
      $scope.context = report.contextData;
      var buckets = report.buckets;
      buckets = _.toPairs(buckets);
      buckets.sort((a, b) => {
          return a[0] - b[0];
      });
      $scope.buckets = buckets;
      $scope.date = report.date;
    });
  PartyCrasher.fetchSummary({ project, id })
    .then(summary => {
      $scope.summary = summary;
    });
});
