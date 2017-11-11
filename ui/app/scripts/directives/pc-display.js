angular.module('PartyCrasherApp')
.directive('pcDisplay', function (
  $location,
  $http,
  $rootScope,
  BASE_HREF,
  REST_BASE,
  $timeout
) {
  function link(scope, element, _attrs) {
    scope.error = null;
    scope.result = null;
    scope.reports = null;
    function got(response) {
      scope.result = response.data;
      if (
        "reports" in scope.result
        && Array.isArray(scope.result.reports)
      ) {
        scope.reports = response.data.reports;
        delete scope.result.reports;
      }
      
      if (
        "auto_summary" in scope.result
      ) {
        delete scope.result.auto_summary;
      }
      if (
        "explanation" in scope.result
      ) {
        delete scope.result.explanation;
      }
      var doneLoading = function() {
        if ($http.pendingRequests.length > 0) {
          $timeout(function() {
            doneLoading();
          }, 1);
        } else {
          scope.loading = false;
        }
      }
      $timeout(function() {
        doneLoading();
      }, 1);
    }
    function gotError(response) {
      scope.loading = false;
      scope.error = response;
    }
    function came() {
      url = $location.absUrl();
      url = url.replace(BASE_HREF, REST_BASE);
      console.log(url);
      scope.loading = true;
      scope.error = null;
      scope.result = null;
      scope.reports = null;
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
