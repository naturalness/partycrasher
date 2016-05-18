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
  restService,
  $location,
  $routeParams,
  $httpParamSerializer
) {
  var url = $location.url();
  $scope.value = 'Loading...';
  restService.getRest('/').then(function (response) {
    var value = response.plain();
    $scope.availableThresholds = value.config.thresholds;
  });
  restService.getRest(url).then(function (response) {
    $scope.value = response.plain();
    $scope.currentThreshold = $scope.value.threshold;
    delete $scope.value.threshold;
  });
  var urlThreshold = $routeParams.threshold;
  var urlProject = $routeParams.project;
  $scope.currentThreshold = urlThreshold;
  $scope.$watch(
    function (scope) { return scope.currentThreshold; },
    function (newThreshold, oldThreshold) {
      if (newThreshold != oldThreshold) {
        var newUrl = '/' + urlProject + '/buckets/'
        + newThreshold + '?'
        + $httpParamSerializer($location.search());
        $location.url(newUrl);
      }
    });
});
