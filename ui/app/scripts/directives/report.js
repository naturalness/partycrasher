angular.module('PartyCrasherApp')
.directive('report', function ($log) {
  function link(scope, element, _attrs) {
    scope.$watch('report', function (report) {
      if (report === undefined) {
        return;
      }
    });
  }
  
  return {
    templateUrl: 'views/report.html',
    link: link,
    restrict: 'E',
    scope: false,
  };
});
