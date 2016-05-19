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
  $httpParamSerializer,
  DEFAULT_THRESHOLD
) {
  var threshold = $routeParams.threshold || DEFAULT_THRESHOLD,
    project = $routeParams.project || '*';

  /* Initially, we're loading. */
  $scope.loading = true;

  $http.get(searchUrl({ project, threshold, since: '2000' })).then(({data}) => {
    $scope.results = data;
    $scope.hasResults = data['top_buckets'].length > 0;
    $scope.loading = false;
  });

  function searchUrl({project, threshold, since}) {
    var query = $httpParamSerializer({ since: since || '3-days-ago' });
    return `/${project}/buckets/${threshold}?${query}`;
  }
});
