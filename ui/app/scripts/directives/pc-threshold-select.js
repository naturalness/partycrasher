/**
 *
 */
angular.module('PartyCrasherApp')
.directive('pcThresholdSelect', function ($log, DEFAULT_THRESHOLD, THRESHOLDS) {
  function sortFloat(a, b) {
    return parseFloat(a) - parseFloat(b);
  }
  THRESHOLDS.sort(sortFloat);
  function link(scope, element, _attrs) {
    var initialThreshold = scope.threshold;

    if (THRESHOLDS.indexOf(DEFAULT_THRESHOLD) < 0) {
      $log.error(`Default threshold (${DEFAULT_THRESHOLD}) is not
                  in the set of available thresholds: ${THRESHOLDS}`);
    }

    scope.thresholds = THRESHOLDS;
    var initialThresholdIndex = thresholdIndex(initialThreshold);
    scope.thresholdIndex = initialThresholdIndex;

    /* Automatically set the threshold to the appropriate value based on the
     * index. */
    scope.$watch('thresholdIndex', (newValue, oldValue) => {
      if (newValue === oldValue) { // On init
        if (initialThreshold == null) {
          scope.thresholdIndex = thresholdIndex(DEFAULT_THRESHOLD);
          scope.threshold = DEFAULT_THRESHOLD;
          console.log("Reset due to initialThreshold null");
        } else {
          scope.thresholdIndex = initialThresholdIndex;
          scope.threshold = initialThreshold;
          console.log("!!!" + initialThreshold + " " + initialThresholdIndex);
        }
        return;
      }
      scope.threshold = THRESHOLDS[newValue];
    });
  }

  function thresholdIndex(threshold) {
    if (threshold == null) {
      return null;
    }
    var index = THRESHOLDS.indexOf(threshold.toString());
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
