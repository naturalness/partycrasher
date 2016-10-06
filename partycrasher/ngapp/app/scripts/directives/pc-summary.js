/**
 * Displays keywords for a crash.
 */
angular.module('PartyCrasherApp')
.directive('pcSummary', function(PartyCrasher, CrashReport) {
  function link(scope, element, _attrs) {
    /* When database-id has stabilized, do a request. */
    scope.$watch('databaseId', function (value) {
      if (value === undefined) {
        return;
      }

      /* Value has stabilized, so we can fetch the summary! */
      PartyCrasher.fetchSummary({ project: scope.project, id: value })
        .then(summary => { scope.summary = groupSummary(summary); });
    });
  }
  
  function groupSummary(summary) {
//     var grouped = _.mapValues(_.groupBy(summary, "term"), (i) =>{
//       return _.sumBy(i, "value");
//     });
//     grouped = _.sortBy(_.toPairs(grouped), 1).reverse();
    var grouped = _.map(summary, (i) => {
      return [i["field"] + ":\"" + i["term"], i["value"]] + "\"";
    });
    grouped = _.sortBy(grouped, 1).reverse();
    
    var head = [];
    var tail = [];
    grouped.forEach (term => {
        if (head.length < 2 
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
      project: '<',
      databaseId: '<'
    }
  };
});

