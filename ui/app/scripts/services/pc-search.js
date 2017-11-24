/**
 * Like $location but does all the partycrasher-specific packing and unpacking.
 * 
 * Patches into a scope's variables:
 *    q - free-text query
 *    project
 *    since
 *    until
 *    from
 *    size
 *    grouping
 */
'use strict';

var canceller;

angular.module('PartyCrasherApp')
.factory('pcSearch', function (
    $rootScope, 
    $location,
    BASE_HREF,
    DEFAULT_THRESHOLD,
    $http,
    $q
  ) {
  canceller = $q.defer();
  $http.defaults['timeout'] = canceller.promise;
//   canceller.promise.then(function() {debugger;});
  
  var state = {}; // shared state pojo

  function read_location() {
    // update shared state from current url
    var pathReportType = [];
    var pathProject = [];
    var pathThreshold = null;
    var pathBucket = null;
    var pathGrouping = null;
    var pathReport = null;
    
    var path = $location.path().split('/');
    for (var i = 1; i < path.length; i++) {
      if (path[i] == "" 
        | path[i] == "projects"
        | path[i] == "types"
        | path[i] == "thresholds"
        | path[i] == "buckets"
        | path[i] == "reports"
      ) {
        null;
      } else if (path[i-1] == 'projects') {
        pathProject = path[i].split(',');
      } else if (path[i-1] == 'types') {
        pathReportType = path[i].split(',');
      } else if (path[i-1] == 'thresholds') {
        pathThreshold = parseFloat(path[i]);
        if (isNaN(pathThreshold)) {
          throw `Bad threshold value ${path[i]}`;
        }
      } else if (path[i-1] == 'buckets') {
        pathBucket = path[i].split(',');
        pathGrouping = 'buckets';
      } else if (path[i-1] == 'reports') {
        pathGrouping = 'reports';
        pathReport = path[i];
      } else {
        throw `Unknown path information ${path[i-1]}/${path[i]}`;
      }
      if (path[path.length-2] == 'buckets') {
        pathGrouping = 'buckets';
      } else if (path[path.length-2] == 'reports') {
        pathGrouping = 'reports';
      }
    }
    state.q = $location.search().q || null;
    state.project = pathProject 
      || $location.search().project || null;
    state.since = $location.search().since;
    state.until = $location.search().until;
    state.from = $location.search().from;
    state.size = $location.search().size;
    state.grouping = pathGrouping ||
      $location.search().grouping || null;
    state.bucket = pathBucket 
      $location.search().bucket || null;
    state.threshold = pathThreshold
      $location.search().threshold || null;
    state.report_type = pathReportType
      || $location.search().type || null;
    state.report = pathReport || null;
  }
  
  read_location(); /* ensure properties exist in state so I don't have to list
                      them again */
  
  function write_location() {
    // update current url from shared state
    var path = "/";
    if (state.report_type.length == 0) {
      path += ``;
    } else {
      path += `types/${state.report_type}/`;
    }
    if (state.project == "*" ||  state.project.length == 0) {
      null;
    } else {
      path += `projects/${state.project}/`;
    }
    if (state.grouping == 'buckets' || state.bucket) {
      if (!state.threshold) {
        state.threshold = DEFAULT_THRESHOLD;
      }
      path += `thresholds/${state.threshold}/`;
    } 
    if (state.bucket) {
      path += `buckets/${state.bucket}/`;
    } 
    if (state.grouping == 'buckets') {
      path += `buckets/`;
    } else if (state.grouping == 'reports') {
      if (state.report) {
        path += `reports/` + state.report + `/`;
      } else {
        path += `reports/`;
      }
    }
    $location.search('q', state.q)
      .search('since', state.since)
      .search('until', state.until)
      .search('from', state.from)
      .search('size', state.size)
      .path(path);
    // TODO
  }
  
  function go() {
    write_location();
  }
  
  write_location(); // ensure early sync -- basically a default route redirect
  
  function came() {
    // watch for url change
    console.log('$locationChangeSuccess changed!', new Date());
    canceller.resolve();
    canceller = $q.defer();
    $http.defaults['timeout'] = canceller.promise;
//     debugger;
//     $http.pendingRequests = [];

    read_location();
    $rootScope.$emit('search-changed');
  }
  
  $rootScope.$on('$locationChangeSuccess', came);
  
  function update_scope(scope) {
    for (let k of Object.keys(state)) {
      scope[k] = state[k];
    }
  }
  
  function make_watcher(k) {
    var p = k;
    console.log('Watching ' + p);
    return function(newValue, oldValue, scope) {
      console.log(newValue + " " + oldValue + " " + p + " " + scope[p] 
        + " " + state[p]);
      if (
        (newValue != oldValue) 
//         && (!Array.isArray(newValue))
      ) { // Don't trigger on init
        if (scope[p] != state[p]) {
          console.log('Changing location... ' 
            + p + " " + scope[p] + " " + state[p]
          );
          state[p] = newValue;
          go();
        }
      }
    };
  }
  
  return {
    link: function(scope) {
      // link given scope to our shared state
      var deregister = $rootScope.$on('search-changed', function() {
        update_scope(scope);
        });
      for (let k of Object.keys(state)) {
        scope[k] = state[k];
        scope.$watch(k, make_watcher(k));
      }
      scope.$on('$destroy', deregister);
    },
  };
});
