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
      scope.stackhead = extractHead(value);
    });
  
    scope.$watch('databaseId', function (value) {
      if (value === undefined) {
        return;
      }
      /* Value has stabilized, so we can fetch the summary! */
      PartyCrasher.fetchReport({ project: scope.project, id: value })
        .then(rawReport => { 
          scope.stackhead = extractHead(new CrashReport(rawReport));
        });
    });
  }
  function extractHead(crash) {
      var stack = crash.stackTrace;
      var head = [];
      
      stack.forEach((frame) => {
          if (frame.func) {
              if (frame._raw['logdf'] > 5) {
                  head.push([frame.func, 'stacktrace.function:'+frame.func]);
              }
          }
      });
      return head;
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

