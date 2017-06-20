/**
 *
 */
angular.module('PartyCrasherApp')
.directive('pcThresholdSelect', function ($log, DEFAULT_THRESHOLD, THRESHOLDS) {
  function link(scope, element, _attrs) {
    var initialThreshold = scope.threshold;
    var initialThresholdSet = false;

    if (thresholdIndex(DEFAULT_THRESHOLD) < 0) {
      $log.error(`Default threshold (${DEFAULT_THRESHOLD}) is not
                  in the set of available thresholds: ${THRESHOLDS}`);
    }

    scope.thresholds = THRESHOLDS;
    var initialThresholdIndex = thresholdIndex(initialThreshold);
    scope.thresholdIndex = initialThresholdIndex;

    /* Automatically set the threshold to the appropriate value based on the
     * index. */
    scope.$watch('thresholdIndex', (newValue, _oldValue) => {
      /** TODO: on-release callback. */
      if (!initialThresholdSet) {
        initialThresholdSet = true;
        scope.thresholdIndex = initialThresholdIndex;
        scope.threshold = initialThreshold;
        return;
      }
      if (newValue != _oldValue) {
        scope.threshold = THRESHOLDS[newValue];
      }
    });
  }

  function thresholdIndex(threshold) {
    var index = THRESHOLDS.indexOf(threshold);
    if (index < 0) {
      /* Return a reasonable default. */
      return THRESHOLDS.indexOf(DEFAULT_THRESHOLD);
    }
    return index;
  }

  return {
    templateUrl: 'views/pc-threshold-select.html',
    restrict: 'E',
    link: link,
    scope: {
      threshold: '='
    }
  };
});
