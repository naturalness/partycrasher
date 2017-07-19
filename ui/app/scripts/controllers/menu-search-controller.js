angular.module('PartyCrasherApp')
.controller('MenuSearchController', function ($scope, $location) {
  function search() {
    var query = $scope.menuSearchQuery;
    $location.$$search = {};
    $location
      .search('q', query)
      .path(`/*/search`);
  }
  
  $scope.search = search;
});
