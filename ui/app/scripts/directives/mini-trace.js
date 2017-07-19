/**
 * Displays a mini stacktrace for a crash.
 */
angular.module('PartyCrasherApp')
.directive('miniTrace', function(PartyCrasher, CrashReport) {
  function link(scope, element, _attrs) {
    /* When database-id has stabilized, do a request. */
    scope.$watch('crash', function (value) {
      if (value === undefined) {
        return;
      }
      [scope.stackhead, scope.stackmore] = extractHead(value);
    });
  
    scope.$watch('databaseId', function (value) {
      if (value === undefined) {
        return;
      }
      /* Value has stabilized, so we can fetch the summary! */
      PartyCrasher.fetchReport({ project: scope.project, id: value })
        .then(rawReport => { 
          [scope.stackhead, scope.stackmore] = extractHead(new CrashReport(rawReport));
        });
    });
  }
  function extractHead(crash) {
      var stack = crash.stackTrace;
      var head = [];
      var more = [];
      
      var maxlogdf = 0.0;
      
      var maxhead = 3;
      var maxmore = 3;
      
      stack.forEach((frame) => {
        if (frame.func) {
          if (parseFloat(frame._raw['logdf']) > maxlogdf) {
            maxlogdf = frame._raw['logdf'];
          }
        }
      });
      
      var started = false;
      
      var i = 0;
      
      stack.forEach((frame) => {
          i = i + 1;
          if (frame.func) {
              var depth = i;
              if (frame._raw['depth']) {
                depth = frame._raw['depth'];
              }
              var prepared = [frame.func, 'stacktrace.function:"'+frame.func+'"', depth];
              var inhead = false;
              if (head.length < maxhead) {
                head.push(prepared);
                inhead = true;
              }
              if (parseFloat(frame._raw['logdf']) > 0.9 * maxlogdf || started) {
                  started = true;
                  if (more.length < maxmore && (! inhead)) {
                      more.push(prepared);
                  }
              }
          }
      });
      if ((more.length > 0) && ((head[head.length-1][2] + 1) >= more[0][2])) {
        head = head.concat(more);
        more = []
      }
      return [head, more];
  }

  return {
    templateUrl: 'views/mini-trace.html',
    link: link,
    scope: {
      crash: '<',
      databaseId: '<',
      project: '<',
    }
  };
});

