'use strict';

/**
 * Displays a mini stacktrace for a crash.
 */
function recursiveArrayEquals(a, b) {
  if (a.length != b.length) {
//     console.log("length " + a.length + " ne " + b.length);
    return false;
  }
  for (var i = 0; i < a.length; i++) {
    if (
      Array.isArray(a[i])
      && Array.isArray(b[i])
    ) {
//       console.log("array ne");
      return recursiveArrayEquals(a[i], b[i]);
    } else if (a[i] != b[i]) {
//       console.log("direct " + a[i] + " ne " + b[i]);
      return false;
    }
  }
  return true;
}

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
    scope.$watch('reports', function (value) {
      if (value === undefined) {
        return;
      }
      $http.get(scope.reports + "?size=100").then(function(response) {
        var stacks = [];
        var votes = [];
//           debugger;
        for (var crash of response.data.reports) {
          var stack = extractHead(crash.report);
          var found = false;
          for (var i = 0; i < stacks.length; i++) {
            if (recursiveArrayEquals(stack, stacks[i])) {
//               debugger;
              votes[i]++;
              found = true;
            }
          }
          if (!found) {
            stacks.push(stack);
            votes.push(1);
          }
        }
        var max = 0;
        var argmax = 0;
        for (var i = 0; i < stacks.length; i++) {
          if (votes[i] > max) { /* always prefer first (most recent) stack */
            max = votes[i];
            argmax = i;
          }
        }
        console.log("Using stack " + argmax + " of " + stacks.length);
        [scope.stackhead, scope.stackmore] = stacks[argmax];
      });
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
      reports: '<',
    }
  };
});

