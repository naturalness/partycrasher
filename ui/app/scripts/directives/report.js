angular.module('PartyCrasherApp')
.directive('report', function (FIXED_FIELDS, $http, DEFAULT_THRESHOLD) {
  function link(scope, element, _attrs) {
    scope.fixed_fields = FIXED_FIELDS;
    scope.$watch('report', function (report) {
      if (report === undefined) {
        return;
      }
      let buckets = Object.assign({}, scope.report.buckets);
      if ('top_match' in buckets) {
        delete buckets.top_match;
      }
      buckets = Object.values(buckets);
      buckets = buckets.sort((a, b) => {
        return parseFloat(a.threshold) - parseFloat(b.threshold);
      });
      scope.bucketMax = 0; 
      for (var i = 0; i < buckets.length; i++) {
        let bucket = buckets[i];
        $http.get(bucket.reports, {timeout: canceller.promise})
          .then(function(response) {
            if (response.data.total > scope.bucketMax) {
              scope.bucketMax = response.data.total;
              scope.logBucketMax = Math.log2(response.data.total);
            }
            bucket.count = response.data.total;
            bucket.logCount = Math.log2(response.data.total);
            if (bucket.threshold == DEFAULT_THRESHOLD) {
              scope.commonReports = response.data.reports;
            }
          });
      }
      scope.buckets = buckets;
      
      scope.precedents = [];
      var getPrecedents = (href, score, limit) => {
        if (limit > 0 && score > DEFAULT_THRESHOLD) {
          $http.get(href, {timeout: canceller.promise})            
            .then(function(response) 
          {
            var precedent = Object.assign({}, response.data);
            precedent['score'] = score;
            scope.precedents.push(precedent);
            if (precedent.report.buckets.top_match) {
              getPrecedents(
                precedent.report.buckets.top_match.href,
                precedent.report.buckets.top_match.score,
                limit - 1
              );
            }
          });
        }
      };
      if (report.buckets.top_match) {
        getPrecedents(
          report.buckets.top_match.href,
          report.buckets.top_match.score,
          10
        );
      }
      
      scope.reportMin = Object.assign({}, report);
      delete scope.reportMin.buckets;
      delete scope.reportMin.project;
      delete scope.reportMin.type;
    });
  }
  
  return {
    templateUrl: 'views/report.html',
    link: link,
    restrict: 'E',
    scope: false,
  };
});
