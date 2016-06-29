angular.module('PartyCrasherApp')
.controller('SearchController', function (
  $scope,
  $location,
  $routeParams,
  PartyCrasher,
  CrashReport
) {
  var q = $routeParams.q;
  var project = $routeParams.project || '*';

  $scope.search = search;
  $scope.search.query = q;
  
  search();
  
  function search() {
    $scope.loading = true;
    var query = $scope.search.query;
    var from = $location.search.from;
    var size = $location.search.size;

    
    PartyCrasher.searchQuery({ project, q, from, size })
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

    $location
      .search('q', query)
      .path('/*/search');
  }
  
  
});
