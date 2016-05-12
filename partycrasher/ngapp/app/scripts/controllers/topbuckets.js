'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:TopbucketsCtrl
 * @description
 * # TopbucketsCtrl
 * Controller of the ngappApp
 */
angular.module('ngappApp')
.controller('TopbucketsCtrl', function ($scope, restService, 
                                        REST_BASE, BASE_HREF, $location,
                                        $routeParams
                                       ) {
    var url = $location.url();
    $scope.value = "Loading...";
    restService.getRest(url).then(function (response) {
        $scope.value = response.plain();
        $scope.currentThreshold = $scope.value.threshold;
        delete $scope.value.threshold;
    });
    $scope.currentThreshold = $routeParams.threshold;
});
