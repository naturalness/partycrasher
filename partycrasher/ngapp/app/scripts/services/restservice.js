'use strict';

/**
 * @ngdoc service
 * @name ngappApp.restService
 * @description
 * # restService
 * Factory in the ngappApp.
 */
angular.module('PartyCrasherApp')
  .factory('restService', ['Restangular', function (Restangular) {
    var service = {
      getRest: getRest,
      getRoot: getRoot
    };
    
    function getRest(url){
      return Restangular.one(url).get();
    }
    function getRoot(){
      return Restangular.one('/').get();
    }
    
    return service;
  }]);
