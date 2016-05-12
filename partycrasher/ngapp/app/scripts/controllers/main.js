'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the ngappApp
 */
angular.module('ngappApp')
  .controller('MainCtrl', function ($scope, restService, REST_BASE, BASE_HREF, $location) {
    var url = $location.url();
    $scope.value = "Loading...";
    restService.getRest(url).then(function (response) {
      $scope.value = response.plain();
    });
  });
