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
  var project = $routeParams.project || '*';

  $scope.projects = PROJECT_NAMES;

  $scope.search = search;
  $scope.search.query = q;
  $scope.search.project = project;

  $scope.loading = true;
  PartyCrasher.searchQuery({ project, q: query, from, size })
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
    var from = $location.search.from || 0;
    var size = $location.search.size || 10;
    $location
      .search('q', query)
      .path(`/${project}/search`);
  }
});
