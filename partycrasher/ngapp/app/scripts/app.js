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
    'restangular'
  ])
  .config(function ($routeProvider, $locationProvider, DEFAULT_THRESHOLD) {
    $routeProvider
      .when('/', {
        /* Redirect to top buckets for ALL projects. */
        redirectTo: `/*/buckets/${DEFAULT_THRESHOLD}`
      })

      /* Top Buckets. */
      .when('/:project?/buckets/:threshold', {
        templateUrl: 'views/top-buckets.html',
        controller: 'TopBucketsController'
      })

      /* View a bucket. */
      .when('/:project?/buckets/:threshold/:id', {
        templateUrl: 'views/view-bucket.html',
        controller: 'BucketController'
      })

      /* TODO: */
      /* View a crash report. */
      .when('/:project?/reports/:id', {
        templateUrl: 'views/not-implemented.html',
        controller: 'NotImplementedController'
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
