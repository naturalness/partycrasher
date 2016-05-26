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
    'ngNamedRoute',
    'datePicker'
  ])
  .config(function ($routeProvider, $locationProvider, DEFAULT_THRESHOLD) {
    $routeProvider
      .when('/', {
        /* Redirect to top buckets for ALL projects. */
        redirectTo: `/*/buckets/${DEFAULT_THRESHOLD}`
      })

      /* Top Buckets. */
      .when('/:project?/buckets/:threshold', {
        name: 'top-buckets',
        templateUrl: 'views/top-buckets.html',
        controller: 'TopBucketsController'
      })

      /* View a bucket. */
      .when('/:project?/buckets/:threshold/:id', {
        name: 'view-bucket',
        templateUrl: 'views/view-bucket.html',
        controller: 'BucketController'
      })

      /* View a crash report. */
      .when('/:project?/reports/:id', {
        name: 'view-report',
        templateUrl: 'views/view-crash.html',
        controller: 'CrashController'
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
