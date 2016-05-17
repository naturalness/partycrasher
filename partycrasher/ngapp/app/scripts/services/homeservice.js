'use strict';

/**
 * @ngdoc service
 * @name ngappApp.homeService
 * @description
 * # homeService
 * Service in the ngappApp.
 */
angular.module('PartyCrasherApp')
  .service('homeService', ['Restangular', function (Restangular) {
    var Home = Restangular.service('home');


    // AngularJS will instantiate a singleton by calling "new" on this function
  }]);
