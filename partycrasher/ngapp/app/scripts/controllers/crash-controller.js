'use strict';

/**
 * @ngdoc function
 * @name ngappApp.controller:CrashController
 * @description
 * # TopbucketsCtrl
 * Controller of the ngappApp
 */
angular.module('PartyCrasherApp')
.controller('CrashController', function (
  $scope,
  $routeParams,
  PartyCrasher,
  CrashReport
) {
  var project = $routeParams.project,
    id = $routeParams.id;
    
  PartyCrasher.fetchReport({ project, id })
    .then(rawReport => {
      var report = $scope.crash = new CrashReport(rawReport);
      $scope.stack = report.stackTrace;
      $scope.context = report.contextData;
      var buckets = report.buckets;
      buckets = _.toPairs(buckets);
      buckets.sort((a, b) => {
          return a[0] - b[0];
      });
      $scope.buckets = buckets;
      $scope.date = report.date;
      
      var precedentId1 = rawReport['buckets']['top_match']['report_id'];
      var precedentProject1 = rawReport['buckets']['top_match']['project'];
      var precedentScore1 = rawReport['buckets']['top_match']['score'];
      
      $scope.precedents = [];
      
      var getPrecedents = (id, project, score, limit) => {
        if (limit > 0) {
          PartyCrasher.fetchReport({id, project})
            .then(rawPrecedent => {
              var precedent = new CrashReport(rawPrecedent);
              precedent['score'] = score;
              $scope.precedents.push(precedent);
              if (rawPrecedent['buckets']['top_match']) {
                var precedentId = rawPrecedent['buckets']['top_match']['report_id'];
                var precedentProject = rawPrecedent['buckets']['top_match']['project'];
                var precedentScore = rawPrecedent['buckets']['top_match']['score'];
                getPrecedents(precedentId, precedentProject, precedentScore, limit -1);
              }
            });
        }
      };
      
      function getBucketTotal(bucket) {
        PartyCrasher.fetchBucket({ 
          project: bucket[1].project,
          threshold: bucket[1].threshold,
          id: bucket[1].id,
          from: 0,
          size: 0 }).then(
          data => {
            bucket[1].total = data['total'];
          })
      }
      
      for (var bucket of buckets) {
        getBucketTotal(bucket);
      }
      
      getPrecedents(precedentId1, precedentProject1, precedentScore1, 10);
      
    });
});
