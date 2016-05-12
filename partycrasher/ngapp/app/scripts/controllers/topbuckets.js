'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:TopbucketsCtrl
 * @description
 * # TopbucketsCtrl
 * Controller of the ngappApp
 */
angular.module('ngappApp')
  .controller('TopbucketsCtrl', function ($scope, restService, REST_BASE, BASE_HREF, $location, $routeParams) {
    var url = $location.url();
    restService.getRest(url).then(function (response) {
      $scope.value = response.plain();
    });
    
    $scope.displayType = function(k, v) {
      if (k == "href") {
        return "link";
      } else if (v instanceof Array) {
        return "array";
      } else if (typeof v == "object") {
        return "dict";
      } else {
        return "default";
      }
    };
    $scope.myIsArray = function(o) {
      return (o instanceof Array);
    };
    $scope.myIsObject = function(o) {
      return (typeof o == "object");
    };
    $scope.uiLink = function(url) {
      return url.replace(REST_BASE, BASE_HREF);
    };
  });
