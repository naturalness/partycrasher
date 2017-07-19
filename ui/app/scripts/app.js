'use strict';

/**
 * @ngdoc overview
 * @name ngappApp
 * @description
 * # ngappApp
 *
 * Main module of the application.
 */
angular
  .module('PartyCrasherApp', [])
  .config(function ($locationProvider) {
    /* Provide routing that looks like natural URLs. */
    $locationProvider.html5Mode({
      enabled: true,
      requireBase: true
    });
  })
  ;
