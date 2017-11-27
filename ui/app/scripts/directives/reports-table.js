angular.module('PartyCrasherApp')
.directive('reportsTable', function ($log, FIXED_FIELDS) {
  function link($scope) {
    $scope.fixed_fields = FIXED_FIELDS;
  }
    
  return {
    templateUrl: 'views/reports-table.html',
    link: link,
    restrict: 'E',
    scope: {
      reports: '<',
    }
  };
});
