/**
 * Bucket summary, for use within a <dl>.
 */
angular.module('PartyCrasherApp')
.directive('pcBucketSummary', function () {
  return {
    restrict: 'E',
    templateUrl: 'views/pc-bucket-summary.html',
    scope: {
      title: '@',
      stats: '<'
    }
  };
});
