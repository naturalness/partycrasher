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
      if (path[i] == "" | path[i] == "project") {
        null;
      } else if (path[i-1] == 'project') {
        pathProject = path[i].split(',');
      } else if (!isNaN(parseFloat(path[i-1]))) {
        pathBucket = path[i];
      } else if (!isNaN(parseFloat(path[i]))) {
        pathThreshold = path[i];
        pathGrouping = "bucket";
      } else if (i == 1) {
        // This must be the last else if
        pathReportType = path[i];
      } else {
        throw `Unknown path information ${path[i-1]}/${path[i]}`;
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
      $location.search().grouping || "report";
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
      path += `*/`;
    } else {
      path += `${state.report_type}/`;
    }
    if (state.project == "*" ||  state.project.length == 0) {
      null;
    } else {
      path += `project/${state.project}/`;
    }
    if (state.bucket) {
      path += `${state.threshold}/${state.bucket}/`;
    } else if (state.threshold != null && state.grouping == 'bucket') {
      path += `${state.threshold}/`;
    } else if (state.grouping == 'bucket') { // threshold must be null
      path += `${DEFAULT_THRESHOLD}/`;
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
