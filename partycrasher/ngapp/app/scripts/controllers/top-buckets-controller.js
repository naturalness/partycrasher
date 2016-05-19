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
  /* TODO: derive this from $routeParams and an AJAX call. */
  Object.assign($scope, {
    since: '2012-05-19T00:00:00Z',
    threshold: '4.0',
    top_buckets: [
      {
        href: 'http://partycrasher.dev/ubuntu/buckets/4.0/add215ee-1fbe-45e5-9ef3-334dc16fcc3f',
        id: 'add215ee-1fbe-45e5-9ef3-334dc16fcc3f',
        project: 'ubuntu',
        threshold: '4.0',
        /* TODO: requires LAST SEEN. */
        last_seen: '2012-07-26T07:20:50Z',
        total: 3
      },
      {
        href: 'http://partycrasher.dev/alan_parsons/buckets/4.0/06080d73-1d33-4969-9d5e-69263cc01752',
        id: '06080d73-1d33-4969-9d5e-69263cc01752',
        project: 'alan_parsons',
        threshold: '4.0',
        total: 1
      },
      {
        href: 'http://partycrasher.dev/alan_parsons/buckets/4.0/0d32cf8a-c1f4-409c-b177-00e693f3dc28',
        id: '0d32cf8a-c1f4-409c-b177-00e693f3dc28',
        project: 'alan_parsons',
        threshold: '4.0',
        total: 1
      },
      {
        href: 'http://partycrasher.dev/alan_parsons/buckets/4.0/10eca7cc-b6d6-44bb-b760-fed7f69c9e8f',
        id: '10eca7cc-b6d6-44bb-b760-fed7f69c9e8f',
        project: 'alan_parsons',
        threshold: '4.0',
        total: 1
      }
    ]
  });

  if (Math.random() < 0) idunnolol();

  function idunnolol() {
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
      (scope) => scope.currentThreshold,
      function (newThreshold, oldThreshold) {
        if (newThreshold != oldThreshold) {
          var query = $httpParamSerializer($location.search());
          var newUrl = `/${urlProject}/buckets/${newThreshold}?${query}`;
          /* Navigate to this URL. */
          $location.url(newUrl);
        }
      });
  }
});
