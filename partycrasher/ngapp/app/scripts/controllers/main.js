'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the ngappApp
 */
angular.module('ngappApp')
  .controller('MainCtrl', ['$scope', 'restService', function ($scope, restService) {
    restService.getRoot().then(function (response) {
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
      return url;
    };
  }]);
