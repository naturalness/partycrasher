angular.module('PartyCrasherApp')
.controller('SearchController', function (
  $scope,
  $location,
  $routeParams,
  PartyCrasher
  
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
          var hits = results['hits'];
          debugger;
          
          $scope.hasResults = hits.length > 0;
          $scope.reports = _.map(hits, '_source');
          $scope.errorMessage = null;
          $scope.loading = false;
      }).catch(error => {
          debugger;
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
