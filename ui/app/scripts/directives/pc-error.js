angular.module('PartyCrasherApp')
.directive('pcError', function (
) {
  function link(scope, element, _attrs) {
    scope.value = scope.error;
    scope.error.headers=scope.error.headers();
  }
  return {
    templateUrl: 'views/pc-error.html',
    link: link,
    scope: false
  };
});
