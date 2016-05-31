

angular.module('PartyCrasherApp')
.directive('pcSummary', function(PartyCrasher) {
  function link(scope, element, attrs) {
    scope.$watch("databaseId", function(value) {
      if (typeof value == "string") {
        PartyCrasher.fetchSummary({ project: scope.project, id: value })
          .then(summary => {
            var grouped = _.mapValues(_.groupBy(summary, "term"), 
                                (i) => {return _.sumBy(i, "value")});
            grouped = _.sortBy(_.toPairs(grouped), 1).reverse();
            var max = grouped[0][1];
            var min = grouped[grouped.length-1][1];
            grouped = _.map(grouped, (i) => {
              i[1] = 192 - _.floor(((i[1]-min)/(max-min)) * 192);
              return i;
            });
            scope.summary = grouped;
          });

//         scope.summary = [{field: "x", term: "fake"}, 
//                           {field: "y", term: value}];
      }
    });
  };
  return {
    templateUrl: 'views/pc-summary.html',
    link: link,
    scope: {
      project: "=",
      databaseId: "=",
    }
  };
});

