angular.module('PartyCrasherApp')
.directive('datey', function ($log) {
  function link(scope, element, attrs) {
    var field = attrs['field'];
    scope.field = field;
    scope.drop = false;
    function watcher(newValue, oldValue, scope) {
      if (newValue === oldValue) { // On init
//         return;
      }
    }
    scope.$watch('value', watcher);
  }

  return {
    templateUrl: 'views/datey.html',
    link: link,
    restrict: 'E',
    scope: {
      value: '=',
    }
  };
});
