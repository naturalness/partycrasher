angular.module('PartyCrasherApp')
.directive('pcDisplay', function (
  $location,
  $http,
  $rootScope,
  BASE_HREF,
  REST_BASE,
  $timeout,
  DEFAULT_THRESHOLD
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
        } else {
          scope[thing] = null;
        }
      }
      function getOutName(thing) {
        if (thing in response.data
          && response.data[thing]
        ) {
          scope[thing] = response.data[thing]["name"];
        } else {
          scope[thing] = null;
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
        } else {
          scope[thing] = null;
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
      getOut("store");
      getOut("version");
      getOut("href");
      getOut("types");
      getOut("projects");
      getOut("config");
      getOut("default_threshold");
      if ('buckets' in response.data 
        && DEFAULT_THRESHOLD in response.data.buckets) {
        $http.get(response.data.buckets[DEFAULT_THRESHOLD]).then(
          function(response) {
            scope.buckets = response.data.buckets;
          }
        );
        delete response.data.buckets;
      }
      if ('reports' in response.data
        && typeof response.data.reports == 'string') {
        $http.get(response.data.reports).then(function(response) {
          scope.reports = response.data.reports;
        });
        delete response.data.reports;
      }        
      if (Object.keys(response.data).length) {
        scope.result = response.data;
      } else {
        scope.result = null;
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
