'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:NavController
 * @description
 * # TopbucketsCtrl
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
.controller('NavController', function ($scope, $route) {
  $scope.isActive = function (name) {
    if (!$route.current) {
      return false;
    }

    return $route.current.name === name;
  };
});
