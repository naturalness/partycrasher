/**
 * Displays keywords for a crash.
 */
angular.module('PartyCrasherApp')
.directive('pcSummary', function($http) {
  function link(scope, element, _attrs) {
    /* When database-id has stabilized, do a request. */
    scope.summary = null;
    scope.$watch('href', function (value) {
      if (value === undefined) {
        return;
      }

      /* Value has stabilized, so we can fetch the summary! */
      $http.get(scope.href + '?explain=true', 
                {timeout: canceller.promise}).then(function(response) {
        scope.summary = groupSummary(response.data.auto_summary);
      });
    });
    scope.$watch('reports', function (value) {
      if (value === undefined) {
        return;
      }
      function from_reports(reports) {
        scope.summary_sum = {};
        for (var crash of reports) {
          $http.get(crash.href + "?explain=true", 
                    {timeout: canceller.promise}).then(function(response) {
            for (var t of response.data.auto_summary) {
              key = t.field + ":" + t.term;
              if (!(key in scope.summary_sum)) {
                scope.summary_sum[key] = {
                  field: t.field,
                  term: t.term,
                  value: 0.0,
                };
              }
              scope.summary_sum[key].value += t.value;
            }
            var sums = Object.values(scope.summary_sum);
            scope.summary = groupSummary(sums);
          });
        }
      }
      if (typeof value === 'string') {
        $http.get(scope.reports + "?size=12", 
                  {timeout: canceller.promise})
        .then(function(response) {
          from_reports(response.data.reports);
        });
      } else {
        from_reports(scope.reports);
      }
    });
  }
  
  function groupSummary(summary) {
//     var grouped = _.mapValues(_.groupBy(summary, "term"), (i) =>{
//       return _.sumBy(i, "value");
//     });
//     grouped = _.sortBy(_.toPairs(grouped), 1).reverse();
    var grouped = _.map(summary, (i) => {
      return [i["field"] + ":" + i["term"], i["value"], i["field"], i["term"]];
    });
    grouped = _.sortBy(grouped, 1).reverse();
    
    var head = [];
    var tail = [];
    grouped.forEach (term => {
        if (head.length < 0 /* dont push stacktrace.function to the top now
                               that mini-trace works */
           && term[0].startsWith("stacktrace.function")) {
             head.push(term);
        } else {
             tail.push(term);
        }
        
    });
    
    grouped = head.concat(tail);
    
    var max = grouped[0][1];
    var min = grouped[grouped.length-1][1];

    return _.map(grouped, (i) => {
      /* Create a greyscale value. */
      i[1] = 192 - _.floor(((i[1]-min)/(max-min)) * 192);
      return i;
    });
  }

  return {
    templateUrl: 'views/pc-summary.html',
    link: link,
    scope: {
      href: '<',
      reports: '<',
    }
  };
});

