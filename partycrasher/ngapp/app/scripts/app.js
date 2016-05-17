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
  .module('PartyCrasherApp', [
    'ngRoute',
    'restangular',
  ])
  .config(function ($routeProvider, $locationProvider) {
    $routeProvider
      .when('/', {
        /* Top buckets for ALL projects. */
        redirectTo: '/*/buckets'
      })
      /* Top Buckets. */
      .when('/:project?/buckets/:threshold?', {
        templateUrl: 'views/topbuckets.html',
        controller: 'TopbucketsCtrl',
        controllerAs: 'main'
      })
      .when('/:project?/buckets/:threshold?/:id', {
        templateUrl: 'views/main.html',
        /* TODO: */
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/:project?/reports/:id', {
        templateUrl: 'views/main.html',
        /* TODO: */
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      /* Unsure? Go to the home page! */
      .otherwise({
        redirectTo: '/'
      });

    /* Provide routing that looks like natural URLs. */
    $locationProvider.html5Mode({
      enabled: true,
      requireBase: true
    });
  });
