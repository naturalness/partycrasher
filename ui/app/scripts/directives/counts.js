angular.module('PartyCrasherApp')
.directive('counts', function ($log) {
  function link(scope, element, _attrs) {
    scope.$watch('counts', function (counts) {
      if (counts === undefined) {
        return;
      }

      for (var f in counts) {
        var a = [];
        for (var k in counts[f]) {
          a.push([k, counts[f][k]]);
        }
        counts[f] = a;
      }
//       debugger;
      scope.counts = counts;
    });
  }
  
  return {
    templateUrl: 'views/counts.html',
    link: link,
    restrict: 'E',
    scope: {
      counts: '<',
    }
  };
});
