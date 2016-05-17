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
  .config(function ($routeProvider, $locationProvider, DEFAULT_THRESHOLD) {
    $routeProvider
      .when('/', {
        /* Redirect to top buckets for ALL projects. */
        redirectTo: `/*/buckets/${DEFAULT_THRESHOLD}`
      })

      /* Top Buckets. */
      .when('/:project?/buckets/:threshold?', {
        templateUrl: 'views/topbuckets.html',
        controller: 'TopbucketsCtrl',
        controllerAs: 'main'
      })

      /* View a bucket. */
      .when('/:project?/buckets/:threshold?/:id', {
        templateUrl: 'views/main.html',
        /* TODO: */
        controller: 'MainCtrl',
        controllerAs: 'main'
      })

      /* View a crash report. */
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
