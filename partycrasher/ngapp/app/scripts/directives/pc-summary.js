

angular.module('PartyCrasherApp')
.directive('pcSummary', function(PartyCrasher) {
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
    var grouped = _.mapValues(_.groupBy(summary, "term"), (i) =>{
      return _.sumBy(i, "value");
    });
    grouped = _.sortBy(_.toPairs(grouped), 1).reverse();
    var max = grouped[0][1];
    var min = grouped[grouped.length-1][1];
    return _.map(grouped, (i) => {
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

