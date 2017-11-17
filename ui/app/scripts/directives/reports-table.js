angular.module('PartyCrasherApp')
.directive('reportsTable', function ($log) {
  return {
    templateUrl: 'views/reports-table.html',
//     link: link,
    restrict: 'E',
    scope: {
      reports: '<',
    }
  };
});
