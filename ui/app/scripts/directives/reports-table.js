angular.module('PartyCrasherApp')
.directive('reports-table', function ($log) {
  return {
    templateUrl: 'views/reports-table.html',
//     link: link,
//     restrict: 'E',
    scope: {
      value: '=',
    }
  };
});
