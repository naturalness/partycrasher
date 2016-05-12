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
      getRoot: getRoot
    };
    
    function getRoot(){
      return Restangular.one('/').get();
    }
    
    return service;
  }]);
