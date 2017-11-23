angular.module('PartyCrasherApp')
.directive('counts', function ($log) {
  return {
    templateUrl: 'views/counts.html',
//     link: link,
    restrict: 'E',
    scope: {
      counts: '<',
    }
  };
});
