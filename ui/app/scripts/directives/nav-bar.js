angular.module('PartyCrasherApp')
.directive('pcNavBar', function ($log, 
                                 DEFAULT_THRESHOLD, 
                                 THRESHOLDS,
                                 COG_IMAGE
                                ) {
  function link(scope, element, _attrs) {
    scope.COG_IMAGE=COG_IMAGE
  }

  return {
    templateUrl: 'views/nav-bar.html',
    link: link,
    scope: false
  };
});
