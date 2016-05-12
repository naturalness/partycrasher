'use strict';

/**
 * @ngdoc service
 * @name ngappApp.restService
 * @description
 * # restService
 * Factory in the ngappApp.
 */
angular.module('ngappApp')
  .factory('restService', ['Restangular', function (Restangular) {
    var service = {
      getRest: getRest
    };
    
    function getRest(url){
      return Restangular.one(url).get();
    }
    
    return service;
  }]);
