'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:PartyCrasherController
 * @description
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
.controller('PartyCrasherController', function (
  $scope,
  pcSearch,
  DEFAULT_THRESHOLD,
  PartyCrasher,
  PROJECT_NAMES
) {
  pcSearch.link($scope);
});
