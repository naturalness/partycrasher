'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:CrashController
 * @description
 * # TopbucketsCtrl
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
.controller('CrashController', function ($scope, CrashReport, SAMPLE_BUCKET) {
  $scope.crash = new CrashReport(SAMPLE_BUCKET['top_reports'][0]);
});
