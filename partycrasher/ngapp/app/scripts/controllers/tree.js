'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:MainCtrl
 * @description
 * # MainCtrl
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
  .controller('TreeCtrl', function ($scope, restService, REST_BASE, BASE_HREF) {
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
    $scope.clicked = function($event) {
      var content = $event.currentTarget.id + '_content';
      $scope.hiddenElts[content] = $scope.hiddenElts[content] ? false : true;
    };
    $scope.hiddenElts = [];
  }).directive('collapsible', function() {
    function link($scope, element, attributes) {
      $scope.hiddenElts[attributes.id] = true;
      $scope.$watch(function(){
        var r = $scope.hiddenElts[attributes.id];
        return r;
      }, function(value) {
        if (typeof value == 'undefined') {
          return;
        }
        if (value) {
          element.show();
        } else {
          element.hide();
        }
      });
    }

    return ({
      link: link
    });
  });
