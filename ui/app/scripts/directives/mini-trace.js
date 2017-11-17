/**
 * Displays a mini stacktrace for a crash.
 */
angular.module('PartyCrasherApp')
.directive('miniTrace', function($http) {
  function link(scope, element, _attrs) {
    /* When database-id has stabilized, do a request. */
    scope.$watch('crash', function (value) {
      if (value === undefined) {
        return;
      }
      [scope.stackhead, scope.stackmore] = extractHead(value);
    });
  }
  function extractHead(crash) {
      var stack = crash.stacktrace;
      var head = [];
      var more = [];
      
      var maxlogdf = 0.0;
      
      var maxhead = 3;
      var maxmore = 3;
      
      stack.forEach((frame) => {
        if (frame.function) {
          if (parseFloat(frame['logdf']) > maxlogdf) {
            maxlogdf = frame['logdf'];
          }
        }
      });
      
      var started = false;
      
      var i = 0;
      
      stack.forEach((frame) => {
          i = i + 1;
          if (frame.function) {
              var depth = i;
              if ('depth' in frame) {
                depth = frame['depth'];
              }
              var prepared = [frame.function, 'stacktrace.function:"'+frame.function+'"', depth];
              var inhead = false;
              if (head.length < maxhead) {
                head.push(prepared);
                inhead = true;
              }
              if (parseFloat(frame['logdf']) > 0.9 * maxlogdf || started) {
                  started = true;
                  if (more.length < maxmore && (! inhead)) {
                      more.push(prepared);
                  }
              }
          }
      });
//       debugger;
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
    }
  };
});

