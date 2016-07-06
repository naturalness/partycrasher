'use strict';

/**
 * Manages the search page and its search results.
 */
angular.module('PartyCrasherApp')
.controller('SearchController', function (
  $scope,
  $location,
  $routeParams,
  PartyCrasher,
  CrashReport,
  PROJECT_NAMES
) {
  var q = $routeParams.q;
  var project = $routeParams.project || null;
  var from = $routeParams.from || 0;
  var size = $routeParams.size || 10;
  var since = $routeParams.since || null;
  var until = $routeParams.until || null;

  $scope.projects = PROJECT_NAMES;

  $scope.search = search;
  $scope.search.query = q;
  $scope.search.project = project;
  $scope.search.from = from | 0; // | 0 coerces to numeric type
  $scope.search.size = size | 0;
  $scope.search.since = since;
  $scope.search.until = until;

  $scope.loading = true;
  PartyCrasher.searchQuery({ project, q, since, until, from, size })
    .then(results => {
      var hits = results;
      var reports = _.map(hits, (c) => {return new CrashReport(c);});
      $scope.hasResults = hits.length > 0;
      $scope.reports = reports;
      $scope.errorMessage = null;
      $scope.loading = false;
    }).catch(error => {
      $scope.hasResults = false;
      $scope.reports = null;
      $scope.errorMessage = error.data.message;
      $scope.loading = false;
    });

  function search() {
    var query = $scope.search.query;
    var project = $scope.search.project;
    var from = $scope.search.from;
    var size = $scope.search.size;
    var since = $scope.search.since;
    var until = $scope.search.until;
    $location
      .search('q', query)
      .search('since', since)
      .search('until', until)
      .search('from', from)
      .search('size', size)
      .path(`/${project}/search`);
  }
  
  function prevPage() {
    $location.search('from',
                     ($scope.search.from | 0) - ($scope.search.size | 0));
  }
  function nextPage() {
    $location.search('from',
                    ($scope.search.from | 0) + ($scope.search.size | 0));
  }

});
