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
) {
  pcSearch.link($scope);
});
