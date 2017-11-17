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
    scope.buckets = null;
    function got(response) {
      function getOut(thing) {
        if (thing in response.data) {
          scope[thing] = response.data[thing];
          delete response.data[thing];
        }
      }
      function getOutName(thing) {
        if (thing in response.data
          && response.data[thing]
        ) {
          scope[thing] = response.data[thing]["name"];
        }
        if (thing in response.data) {
          delete response.data[thing];
        }
      }
      function getOutArray(thing) {
        if (thing in response.data
          && Array.isArray(response.data[thing])
        ) {
          scope[thing] = response.data[thing];
          delete response.data[thing];
        }
      }
      getOutArray("reports");
      getOutArray("buckets");
      getOut("auto_summary");
      getOut("explanation");
      getOut("from");
      getOut("size");
      getOut("next_page");
      getOut("prev_page");
      getOut("total");
      getOutName("type");
      getOutName("project");
      getOut("since");
      getOut("until");
      getOut("bucket_id");
      getOut("threshold");
      getOut("query_string");
      getOut("search");
      scope.result = response.data;
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
      scope.buckets = null;
      $http.get(url).then(got, gotError);
    }
    $rootScope.$on('$locationChangeSuccess', came);
    came();
  }
  return {
    templateUrl: 'views/pc-display.html',
    link: link,
    scope: true
  };
});
