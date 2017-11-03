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
angular.module('PartyCrasherApp')
.factory('pcSearch', function (
    $rootScope, 
    $location, 
    BASE_HREF,
    DEFAULT_THRESHOLD
  ) {
  var state = {}; // shared state pojo

  function read_location() {
    // update shared state from current url
    var pathReportType = [];
    var pathProject = [];
    var pathThreshold = null;
    var pathBucket = null;
    var pathGrouping = null;
    
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
        pathReportThreshold = parseFloat(path[i]);
        if (isNaN(pathReportThreshold)) {
          throw `Bad threshold value ${path[i]}`;
        }
      } else if (path[i-1] == 'buckets') {
        pathBucket = path[i].split(',');
      } else {
        throw `Unknown path information ${path[i-1]}/${path[i]}`;
      }
      if (path[path.length-2] == 'buckets') {
        pathGrouping = 'bucket';
      } else if (path[path.length-2] == 'reports') {
        pathGrouping = 'report';
      }
    }
    state.q = $location.search().q || null;
    state.project = pathProject 
      || $location.search().project || '*';
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
      || $location.search().type || '*';
  }
  
  read_location(); /* ensure properties exist in state so I don't have to list
                      them again */
  
  function write_location() {
    // update current url from shared state
    // console.log('Changing location...');
    path = "/";
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
    if (state.bucket) {
      path += `buckets/${state.bucket}/`;
    } 
    if (state.grouping == 'bucket') {
      if (state.threshold) {
        path += `thresholds/${state.threshold}/`;
      } else { // threshold must be null
        path += `thresholds/${DEFAULT_THRESHOLD}/`;
      }
      path += `buckets/`
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
    //console.log('$locationChangeSuccess changed!', new Date());
    read_location();
    $rootScope.$emit('search-changed');
  }
  
  $rootScope.$on('$locationChangeSuccess', came);
  
  function update_scope(scope) {
    for (let k of Object.keys(state)) {
      scope[k] = state[k];
//       scope.$digest();
    }
  }
  
  function make_watcher(k) {
    var p = k;
    return function(newValue, oldValue, scope) {
      if (newValue !== oldValue) { // Don't trigger on init
        if (scope[p] != state[p]) {
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
