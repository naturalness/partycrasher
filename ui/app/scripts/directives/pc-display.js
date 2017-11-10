angular.module('PartyCrasherApp')
.directive('pcDisplay', function (
  $location,
  $http,
  $rootScope
) {
  function link(scope, element, _attrs) {
    scope.loading = false;
    scope.error = null;
    scope.result = null;
    scope.reports = null;
    function got(response) {
      scope.loading = false;
      scope.result = response.data;
      if ("reports" in scope.result) {
        scope.reports = response.data.reports;
        delete response.data.reports;
      }
    }
    function gotError(response) {
      scope.loading = false;
      scope.error = response;
    }
    function came() {
      url = $location.absUrl();
      url = url.replace(/\/ui\//, "/");
      console.log(url);
      scope.loading = true;
      $http.get(url).then(got, gotError);
    }
    $rootScope.$on('$locationChangeSuccess', came);
    came();
  }
  return {
    templateUrl: 'views/pc-display.html',
    link: link,
    scope: false
  };
});
