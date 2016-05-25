'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:NavController
 * @description
 * # TopbucketsCtrl
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
.controller('NavController', function ($scope, $route, namedRouteService) {
  $scope.isActive = function (name) {
    if (!$route.current) {
      return false;
    }

    return $route.current.name === name;
  };

  $scope.urlFor = function (name, args) {
    /* Reverse the link, but remove the leading forward slash. */
    return namedRouteService.reverse(name, args).substr(1);
  };
});
