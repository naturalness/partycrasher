angular.module('PartyCrasherApp')
.directive('bucketsTable', function ($log) {
  return {
    templateUrl: 'views/buckets-table.html',
//     link: link,
    restrict: 'E',
    scope: {
      buckets: '<',
    }
  };
});
